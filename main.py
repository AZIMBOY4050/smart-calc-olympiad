from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import math
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def serve_html():
    return FileResponse("index.html")

# --- МОДЕЛИ ДАННЫХ ---
class QuadraticEq(BaseModel):
    a: float; b: float; c: float; lang: str = 'ru'

class LinearEq(BaseModel):
    a: float; b: float; lang: str = 'ru'

class Geometry(BaseModel):
    shape: str; a: float; b: float; lang: str = 'ru'

class SystemEq(BaseModel):
    a1: float; b1: float; c1: float
    a2: float; b2: float; c2: float
    lang: str = 'ru'

class Progression(BaseModel):
    a1: float; d: float; n: int
    lang: str = 'ru'

def t(lang, ru, uz, en):
    if lang == 'uz': return uz
    if lang == 'en': return en
    return ru

# --- 1. КВАДРАТНЫЕ УРАВНЕНИЯ ---
@app.post("/solve_quadratic")
def solve_quadratic(eq: QuadraticEq):
    a, b, c, l = eq.a, eq.b, eq.c, eq.lang
    if a == 0:
        return {"steps": [t(l, "Коэффициент 'a' = 0. Это линейное уравнение!", "'a' koeffitsiyenti 0 ga teng. Bu chiziqli tenglama!", "Coefficient 'a' = 0. This is a linear equation!")]}

    steps = [f"{t(l, 'Уравнение', 'Tenglama', 'Equation')}: {a}x² + ({b})x + ({c}) = 0"]
    d = b**2 - 4*a*c
    steps.append(f"D = b² - 4ac = {d}")
    ans = t(l, "Ответ", "Javob", "Answer")

    if d > 0:
        x1 = (-b + math.sqrt(d)) / (2*a)
        x2 = (-b - math.sqrt(d)) / (2*a)
        steps.append(f"x₁ = {x1:.2f}, x₂ = {x2:.2f}")
        steps.append(f"{ans}: x₁ = {x1:.2f}, x₂ = {x2:.2f}")
    elif d == 0:
        x = -b / (2*a)
        steps.append(f"{ans}: x = {x:.2f}")
    else:
        steps.append(t(l, "D < 0. Действительных корней нет.", "D < 0. Haqiqiy ildizlar yo'q.", "D < 0. No real roots."))
    return {"steps": steps}

# --- 2. ЛИНЕЙНЫЕ УРАВНЕНИЯ ---
@app.post("/solve_linear")
def solve_linear(eq: LinearEq):
    a, b, l = eq.a, eq.b, eq.lang
    if a == 0:
        return {"steps": [t(l, "Ошибка: 'a' не может быть 0!", "Xato: 'a' 0 bo'lishi mumkin emas!", "Error: 'a' cannot be 0!")]}
    
    steps = [f"{t(l, 'Уравнение', 'Tenglama', 'Equation')}: {a}x + ({b}) = 0"]
    x = -b / a
    steps.append(f"{a}x = {-b}")
    steps.append(f"{t(l, 'Ответ', 'Javob', 'Answer')}: x = {x:.2f}")
    return {"steps": steps}

# --- 3. ГЕОМЕТРИЯ ---
@app.post("/solve_geometry")
def solve_geometry(geo: Geometry):
    shape, a, b, l = geo.shape, geo.a, geo.b, geo.lang
    steps = []
    if a <= 0 or b <= 0: return {"steps": [t(l, "Ошибка: Стороны должны быть > 0", "Xato: Tomonlar > 0 bo'lishi kerak", "Error: Sides must be > 0")]}
    ans = t(l, "Ответ", "Javob", "Answer")

    if shape == "rectangle":
        steps.append(f"{ans}: S = {a*b}, P = {2*(a+b)}")
    elif shape == "triangle":
        c = math.sqrt(a**2 + b**2)
        steps.append(f"{ans}: S = {(a*b)/2}, P ≈ {(a+b+c):.2f}")
    return {"steps": steps}

# --- 4. СИСТЕМЫ УРАВНЕНИЙ ---
@app.post("/solve_system")
def solve_system(eq: SystemEq):
    l = eq.lang
    steps = [f"1) {eq.a1}x + {eq.b1}y = {eq.c1}", f"2) {eq.a2}x + {eq.b2}y = {eq.c2}"]
    det = eq.a1 * eq.b2 - eq.a2 * eq.b1
    det_x = eq.c1 * eq.b2 - eq.c2 * eq.b1
    det_y = eq.a1 * eq.c2 - eq.a2 * eq.c1
    steps.append(f"D = {det}, Dx = {det_x}, Dy = {det_y}")
    
    ans = t(l, "Ответ", "Javob", "Answer")
    if det == 0:
        steps.append(t(l, "Решений нет или их бесконечно много", "Yechim yo'q yoki cheksiz", "No solutions or infinite solutions"))
    else:
        x = det_x / det
        y = det_y / det
        steps.append(f"{ans}: x = {x:.2f}, y = {y:.2f}")
    return {"steps": steps}

# --- 5. ПРОГРЕССИИ ---
@app.post("/solve_progression")
def solve_progression(pr: Progression):
    l = pr.lang
    steps = [f"a₁ = {pr.a1}, d = {pr.d}, n = {pr.n}"]
    an = pr.a1 + (pr.n - 1) * pr.d
    sn = ((2 * pr.a1 + (pr.n - 1) * pr.d) / 2) * pr.n
    ans = t(l, "Ответ", "Javob", "Answer")
    steps.append(f"aₙ = {an}")
    steps.append(f"Sₙ = {sn}")
    steps.append(f"{ans}: aₙ = {an}, Sₙ = {sn}")
    return {"steps": steps}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)