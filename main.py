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

# --- ГЛАВНАЯ СТРАНИЦА (Отдает HTML файл) ---
@app.get("/")
def serve_html():
    return FileResponse("index.html")

# --- МОДЕЛИ ДАННЫХ ---
class QuadraticEq(BaseModel):
    a: float
    b: float
    c: float
    lang: str = 'ru'

class LinearEq(BaseModel):
    a: float  
    b: float
    lang: str = 'ru'

class Geometry(BaseModel):
    shape: str 
    a: float
    b: float
    lang: str = 'ru'

# Функция перевода
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
    steps.append(f"D = b² - 4ac = ({b})² - 4*({a})*({c})")
    steps.append(f"D = {d}")

    ans = t(l, "Ответ", "Javob", "Answer")

    if d > 0:
        x1 = (-b + math.sqrt(d)) / (2*a)
        x2 = (-b - math.sqrt(d)) / (2*a)
        steps.append(f"x₁ = (-b + √D) / 2a = {x1:.2f}")
        steps.append(f"x₂ = (-b - √D) / 2a = {x2:.2f}")
        steps.append(f"{ans}: x₁ = {x1:.2f}, x₂ = {x2:.2f}")
    elif d == 0:
        x = -b / (2*a)
        steps.append(f"x = -b / 2a = {x:.2f}")
        steps.append(f"{ans}: x = {x:.2f}")
    else:
        steps.append(t(l, "D < 0. Действительных корней нет.", "D < 0. Haqiqiy ildizlar yo'q.", "D < 0. No real roots."))
    
    return {"steps": steps}

# --- 2. ЛИНЕЙНЫЕ УРАВНЕНИЯ ---
@app.post("/solve_linear")
def solve_linear(eq: LinearEq):
    a, b, l = eq.a, eq.b, eq.lang
    if a == 0:
        return {"steps": [t(l, "Ошибка: Коэффициент при 'x' не может быть нулем!", "Xato: 'x' oldidagi koeffitsiyent nol bo'lishi mumkin emas!", "Error: Coefficient of 'x' cannot be zero!")]}
    
    steps = [f"{t(l, 'Уравнение', 'Tenglama', 'Equation')}: {a}x + ({b}) = 0"]
    steps.append(f"{t(l, 'Переносим число вправо', 'Sonni o\'ngga o\'tkazamiz', 'Move number to the right')}: {a}x = {-b}")
    x = -b / a
    steps.append(f"{t(l, 'Делим на', 'Bo\'lamiz', 'Divide by')} {a}: x = {-b} / {a}")
    steps.append(f"{t(l, 'Ответ', 'Javob', 'Answer')}: x = {x:.2f}")
    
    return {"steps": steps}

# --- 3. ГЕОМЕТРИЯ (Площадь и Периметр) ---
@app.post("/solve_geometry")
def solve_geometry(geo: Geometry):
    shape, a, b, l = geo.shape, geo.a, geo.b, geo.lang
    steps = []

    if a <= 0 or b <= 0:
         return {"steps": [t(l, "Ошибка: Стороны фигуры должны быть больше нуля!", "Xato: Shaklning tomonlari noldan katta bo'lishi kerak!", "Error: Shape sides must be greater than zero!")]}

    ans = t(l, "Ответ", "Javob", "Answer")

    if shape == "rectangle":
        steps.append(f"{t(l, 'Фигура: Прямоугольник', 'Shakl: To\'rtburchak', 'Shape: Rectangle')}")
        steps.append(f"{t(l, 'Стороны', 'Tomonlar', 'Sides')}: a = {a}, b = {b}")
        s = a * b
        p = 2 * (a + b)
        steps.append(f"{t(l, 'Площадь', 'Yuza', 'Area')} S = a * b = {a} * {b}")
        steps.append(f"{t(l, 'Периметр', 'Perimetr', 'Perimeter')} P = 2 * (a + b) = 2 * ({a} + {b})")
        steps.append(f"{ans}: {t(l, 'Площадь', 'Yuza', 'Area')} S = {s}, {t(l, 'Периметр', 'Perimetr', 'Perimeter')} P = {p}")

    elif shape == "triangle":
        steps.append(f"{t(l, 'Фигура: Прямоугольный треугольник', 'Shakl: To\'g\'ri burchakli uchburchak', 'Shape: Right Triangle')}")
        steps.append(f"{t(l, 'Катеты', 'Katetlar', 'Legs')}: a = {a}, b = {b}")
        s = (a * b) / 2
        c = math.sqrt(a**2 + b**2)
        p = a + b + c
        steps.append(f"{t(l, 'Площадь', 'Yuza', 'Area')} S = (a * b) / 2 = ({a} * {b}) / 2")
        steps.append(f"{t(l, 'Гипотенуза', 'Gipotenuza', 'Hypotenuse')} c = √(a² + b²) = √({a}² + {b}²) ≈ {c:.2f}")
        steps.append(f"{t(l, 'Периметр', 'Perimetr', 'Perimeter')} P = a + b + c ≈ {p:.2f}")
        steps.append(f"{ans}: {t(l, 'Площадь', 'Yuza', 'Area')} S = {s}, {t(l, 'Периметр', 'Perimetr', 'Perimeter')} P ≈ {p:.2f}")
    else:
        steps.append(t(l, "Ошибка: Неизвестная фигура.", "Xato: Noma'lum shakl.", "Error: Unknown shape."))

    return {"steps": steps}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)