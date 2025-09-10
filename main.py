from app import Enrutador

# Handlers reales
def h_saludo(ctx): return "¡Hola! ¿En qué te ayudo?"
def h_precio(ctx): return "Plan Básico $X/mes, Pro $Y/mes, Equipo $Z/mes."
def h_soporte(ctx): return "Cuéntame el problema y te guío paso a paso."
def h_despedida(ctx): return "¡Hasta luego! 🌙"
def h_default(ctx): return f"(Default) No entendí: {ctx['text']} [razón: {ctx.get('reason')}]"

router = Enrutador()
router.load("intent_router.joblib")

# Reinyecta handlers y fallback
router.handlers.update({
    "saludo": h_saludo,
    "precio": h_precio,
    "soporte": h_soporte,
    "despedida": h_despedida,
})
router.set_fallback(h_default)

# Pruebas
tests = [
    "hola buenos días",
    "oye, ¿cuánto cuesta el plan pro?",
    "tengo un error al iniciar sesión",
    "gracias, nos vemos",
    "gato",                     # <- ruido, debería ir a default
    "mañana quiero comer pizza" # <- ruido, default también
]

for t in tests:
    res = router.route(t)  # aplica gating proba/sim/margen
    print(f"[{t}] -> intent={res.intent} score={res.score:.3f}\n{res.output}\n") # type: ignore
