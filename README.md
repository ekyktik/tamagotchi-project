# 🐾 Піксель — Віртуальний Тамагочі

Міні-проєкт у рамках ІНДЗ-4 (Vibe-кодинг).  
Цифровий вихованець з REST API на FastAPI та пікселарт-фронтендом.

---

## Функціонал

- **Годувати** — вибір типу їжі (звичайна / ласощі / корисна)
- **Грати** — вибір активності (м'ячик / головоломка / танці)
- **Спати** — відновлення енергії
- **Перевірити стан** — поточні показники (голод, щастя, енергія)
- **Скинути** — відродити тамагочі

Кожна дія — це REST-запит до бекенду.

---

## Структура проєкту

```
tamagotchi/
├── backend/
│   ├── main.py          # FastAPI додаток + CORS
│   ├── models.py        # Pydantic моделі
│   ├── routes.py        # Ендпоінти
│   └── requirements.txt
├── frontend/
│   └── index.html       # SPA з fetch API
└── README.md
```

---

## Як запустити локально

### 1. Бекенд

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API буде доступне на: `http://localhost:8000`  
Swagger UI: `http://localhost:8000/docs`

### 2. Фронтенд

Відкрити `frontend/index.html` у браузері.  
Або запустити dev-сервер:

```bash
cd frontend
python -m http.server 5500
```

Потім відкрити: `http://localhost:5500`

---

## API Ендпоінти

| Метод  | Шлях               | Опис                   |
|--------|--------------------|------------------------|
| GET    | /api/v1/status     | Отримати стан тамагочі |
| POST   | /api/v1/feed       | Погодувати             |
| POST   | /api/v1/play       | Пограти                |
| POST   | /api/v1/sleep      | Покласти спати         |
| DELETE | /api/v1/reset      | Скинути до початку     |

### Приклад запиту

```bash
curl -X POST http://localhost:8000/api/v1/feed \
  -H "Content-Type: application/json" \
  -d '{"food_type": "treat"}'
```

---

## Деплой

- **Бекенд** → [Render.com](https://render.com) або [Railway.app](https://railway.app)
- **Фронтенд** → [GitHub Pages](https://pages.github.com) або [Vercel](https://vercel.com)

---

## GitHub Workflow

1. Форкнути репозиторій
2. Кожна фіча у власній гілці: `feat/feed-endpoint`
3. Pull Request → рев'ю → merge в `main`

---

## Технології

- **Backend**: Python 3.12, FastAPI, Pydantic v2, Uvicorn
- **Frontend**: Vanilla HTML/CSS/JS, Fetch API, CSS animations
- **Документація**: Swagger UI (вбудована в FastAPI)