from app.Enrutador import Enrutador

router = Enrutador()

router.add_intent("saludo", [
    "hola", "buenos dias", "buenas", "que onda", "hey", "holi",
    "que tal", "buenas tardes", "buenas noches", "saludos"
], lambda ctx: "dummy")

router.add_intent("precio", [
    "precio", "precios", "cuanto cuesta", "tarifas", "planes", "plan pro",
    "plan mas barato", "suscripcion", "costo mensual"
], lambda ctx: "dummy")

router.add_intent("soporte", [
    "ayuda", "soporte", "no funciona", "tengo un error", "error al iniciar sesion",
    "problema con la cuenta", "no puedo entrar", "bug", "se cayo el sistema"
], lambda ctx: "dummy")

router.add_intent("despedida", [
    "adios", "gracias, hasta luego", "nos vemos", "bye", "hasta pronto", "chao"
], lambda ctx: "dummy")

# Reglas simples (se aplican antes del modelo)
router.add_regex_rule(r"\b(precio|cuan?to cuesta|tarifa|planes?)\b", "precio")
router.add_regex_rule(r"\b(hola|buenas|hey|que onda|saludos)\b", "saludo")
router.add_regex_rule(r"\b(adios|nos vemos|bye|hasta pronto|chao)\b", "despedida")
router.add_regex_rule(r"\b(error|no funciona|soporte|no puedo entrar|bug|fallo)\b", "soporte")

router.train()
router.save("intent_router.joblib")

print("Modelo entrenado y guardado.")