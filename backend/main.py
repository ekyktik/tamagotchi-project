from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

app = FastAPI(
    title="🐾 Virtual Tamagotchi API",
    description="""
## Віртуальний тамагочі — REST API

Доглядайте за вашим цифровим вихованцем Пікселем!

### Ендпоінти
- **GET /status** — перевірити стан тамагочі
- **POST /feed** — погодувати (basic / treat / healthy)
- **POST /play** — пограти (ball / puzzle / dance)
- **POST /sleep** — покласти спати
- **DELETE /reset** — відродити тамагочі

### Показники
Кожен показник від 0 до 100:
- **hunger**: 0 = ситий, 100 = дуже голодний
- **happiness**: 0 = сумний, 100 = щасливий
- **energy**: 0 = втомлений, 100 = бадьорий
""",
    version="1.0.0",
    contact={"name": "Tamagotchi Team", "email": "pixel@tamagotchi.dev"},
)

# CORS — дозволяємо фронтенду звертатись до API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1", tags=["Tamagotchi"])


@app.get("/", tags=["Root"])
def root():
    """Кореневий ендпоінт — базова інформація про API"""
    return {
        "name": "Virtual Tamagotchi API",
        "version": "1.0.0",
        "docs": "/docs",
        "status_endpoint": "/api/v1/status",
    }