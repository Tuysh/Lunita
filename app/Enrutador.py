# En Enrutador.py
from unidecode import unidecode
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
import numpy as np
import joblib, re

def normalize(text: str) -> str:
    return unidecode(text.lower())

class Enrutador:
    def __init__(self):
        self.regex_rules = []          # [(compiled_regex, intent)]
        self.handlers = {}
        self._X, self._y = [], []
        self.pipeline: Pipeline | None = None
        self._tfidf_matrix = None      # matriz de entrenamiento
        self._labels = None            # np.array de labels por fila en _tfidf_matrix
        self.fallback_handler = lambda ctx: "No entendí bien, ¿puedes decirlo de otra forma?"

    def add_intent(self, name, examples, handler):
        self.handlers[name] = handler
        for ex in examples:
            self._X.append(ex)
            self._y.append(name)

    def add_regex_rule(self, pattern: str, intent: str, flags=re.I):
        self.regex_rules.append((re.compile(pattern, flags), intent))

    def set_fallback(self, fn): self.fallback_handler = fn

    def train(self):
        if not self._X: raise ValueError("No hay ejemplos para entrenar.")
        # Vectorizador + SVM + calibración (probabilidades)
        vectorizer = TfidfVectorizer(preprocessor=normalize, ngram_range=(1,2), min_df=1)
        base_svm = LinearSVC()
        calibrated = CalibratedClassifierCV(base_svm, cv=3)  # Platt
        self.pipeline = Pipeline([("tfidf", vectorizer), ("clf", calibrated)])
        self.pipeline.fit(self._X, self._y)

        # Guarda matriz TF-IDF de entrenamiento para similitud
        tfidf = self.pipeline.named_steps["tfidf"]
        self._tfidf_matrix = tfidf.transform(self._X)
        self._labels = np.array(self._y)

    def save(self, path="intent_router.joblib"):
        if self.pipeline is None: raise RuntimeError("Nada que guardar.")
        joblib.dump({
            "pipeline": self.pipeline,
            "regex_serialized": [(p.pattern, i) for p, i in self.regex_rules],
            # almacenamos ejemplos para similitud (ligero) — o solo sus TF-IDF
            "X": self._X, "y": self._y
        }, path)

    def load(self, path="intent_router.joblib"):
        data = joblib.load(path)
        self.pipeline = data["pipeline"]
        self.regex_rules = [(re.compile(p, re.I), i) for p, i in data.get("regex_serialized", [])]
        self._X = data.get("X", [])
        self._y = data.get("y", [])
        # reconstruye la matriz TF-IDF con esos ejemplos
        if self._X:
            tfidf = self.pipeline.named_steps["tfidf"] # type: ignore
            self._tfidf_matrix = tfidf.transform(self._X)
            self._labels = np.array(self._y)

    def route(self, text: str,
              PROBA_MIN: float = 0.55,
              SIM_MIN: float = 0.15,
              MARGIN_MIN: float = 0.0):
        norm = normalize(text)

        # 0) Reglas (sobre normalizado)
        for rx, intent in self.regex_rules:
            if rx.search(norm):
                return self._dispatch(intent, text, score=1.0)

        if self.pipeline is None:
            raise RuntimeError("Modelo no entrenado/cargado.")

        vec = self.pipeline.named_steps["tfidf"].transform([text])
        clf = self.pipeline.named_steps["clf"]

        # A) Probabilidades calibradas
        proba = clf.predict_proba(vec)[0]            # shape (n_clases,)
        classes = clf.classes_
        top_idx = int(np.argmax(proba))
        top_label = classes[top_idx]
        top_proba = float(proba[top_idx])

        # B) Margen (distance to hyperplane del SVM "prefit" dentro de Calibrated)
        #   No siempre está expuesto directo; usamos decision_function del calibrado si existe.
        try:
            decision = clf.decision_function(vec)
            decision = np.atleast_2d(decision)[0]
            top_margin = float(decision[top_idx]) if decision.ndim == 1 or decision.shape[0] == len(classes) else 0.0
        except Exception:
            top_margin = 0.0

        # C) Similitud coseno contra ejemplos (máxima global y por clase)
        max_cos = 0.0
        max_cos_same_class = 0.0
        if self._tfidf_matrix is not None:
            # cos( A,B ) = (A·B) / (||A|| * ||B||) — scipy sparse friendly
            num = (self._tfidf_matrix @ vec.T).toarray().ravel()  # dot a cada ejemplo
            denom = np.linalg.norm(self._tfidf_matrix.toarray(), axis=1) * np.linalg.norm(vec.toarray())
            with np.errstate(divide='ignore', invalid='ignore'):
                cosines = np.where(denom > 0, num / denom, 0.0)
            max_cos = float(np.max(cosines)) if cosines.size else 0.0
            # por clase predicha
            if cosines.size:
                mask = (self._labels == top_label)
                if np.any(mask):
                    max_cos_same_class = float(np.max(cosines[mask]))

        # GATE: si falla cualquiera de estas condiciones → default
        # 1) probabilidad suficientemente alta
        if top_proba < PROBA_MIN:
            return self._default(text, reason=f"low_proba {top_proba:.3f}")

        # 2) margen no negativo (clasificación convincente)
        if top_margin < MARGIN_MIN:
            return self._default(text, reason=f"neg_margin {top_margin:.3f}")

        # 3) similitud mínima con ejemplos (global o por clase)
        if max_cos < SIM_MIN and max_cos_same_class < SIM_MIN:
            return self._default(text, reason=f"low_sim max={max_cos:.3f} class={max_cos_same_class:.3f}")

        # pasa el gate → despacha
        if top_label in self.handlers:
            return self._dispatch(top_label, text, score=top_proba)

        # si no hay handler para esa intent, default
        return self._default(text, reason="no_handler")

    def _dispatch(self, intent, text, score):
        fn = self.handlers.get(intent, self.fallback_handler)
        out = fn({"text": text, "intent": intent, "score": score})
        return type("RouteResult", (), {"intent": intent, "score": score, "output": out})

    def _default(self, text, reason=""):
        out = self.fallback_handler({"text": text, "intent": "default", "score": 0.0, "reason": reason})
        return type("RouteResult", (), {"intent": "default", "score": 0.0, "output": out})
