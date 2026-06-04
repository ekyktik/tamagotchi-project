from fastapi import APIRouter, HTTPException
from datetime import datetime
from models import TamagotchiState, FeedRequest, PlayRequest, StatusResponse, ActionResponse

router = APIRouter()

# Стан тамагочі (в пам'яті — для простоти)
_state = TamagotchiState()


def _get_mood(state: TamagotchiState) -> tuple[str, str]:
    """Визначає настрій та емодзі на основі показників"""
    if not state.is_alive:
        return "спить вічним сном", "💀"

    score = (state.happiness + (100 - state.hunger) + state.energy) / 3

    if score >= 80:
        return "чудовий", "🤩"
    elif score >= 60:
        return "гарний", "😊"
    elif score >= 40:
        return "нейтральний", "😐"
    elif score >= 20:
        return "поганий", "😟"
    else:
        return "жахливий", "😵"


def _to_response(state: TamagotchiState) -> StatusResponse:
    mood, emoji = _get_mood(state)
    return StatusResponse(
        name=state.name,
        hunger=state.hunger,
        happiness=state.happiness,
        energy=state.energy,
        age=state.age,
        is_alive=state.is_alive,
        mood=mood,
        emoji=emoji,
        last_updated=state.last_updated,
    )


def _check_alive(state: TamagotchiState):
    """Перевіряє чи жива тваринка"""
    if not state.is_alive:
        raise HTTPException(status_code=400, detail="Тамагочі вже не живий 😢")


@router.get("/status", response_model=StatusResponse, summary="Отримати стан тамагочі")
def get_status():
    """
    **GET /status** — повертає поточний стан тамагочі.
    
    Показники:
    - `hunger` (0–100): 0 = ситий, 100 = дуже голодний
    - `happiness` (0–100): 0 = сумний, 100 = щасливий  
    - `energy` (0–100): 0 = втомлений, 100 = бадьорий
    """
    # Старіємо на 1 хвилину кожен раз при перевірці
    _state.age += 1

    # Природне погіршення показників
    _state.hunger = min(100, _state.hunger + 2)
    _state.happiness = max(0, _state.happiness - 1)
    _state.energy = max(0, _state.energy - 1)
    _state.last_updated = datetime.now().isoformat()

    # Перевірка на смерть
    if _state.hunger >= 100 and _state.happiness <= 0:
        _state.is_alive = False

    return _to_response(_state)


@router.post("/feed", response_model=ActionResponse, summary="Погодувати тамагочі")
def feed(request: FeedRequest):
    """
    **POST /feed** — годує тамагочі.
    
    Типи їжі:
    - `basic` — звичайна їжа (-20 голод, -5 щастя через нудоту)
    - `treat` — ласощі (-10 голод, +20 щастя, +5 енергія)
    - `healthy` — корисна їжа (-30 голод, +5 щастя, +10 енергія)
    """
    _check_alive(_state)

    valid_foods = ["basic", "treat", "healthy"]
    if request.food_type not in valid_foods:
        raise HTTPException(
            status_code=422,
            detail=f"Невідомий тип їжі '{request.food_type}'. Доступні: {valid_foods}"
        )

    messages = {
        "basic": "Піксель жує звичайну їжу 🍽️",
        "treat": "Піксель обожнює ласощі! 🍬",
        "healthy": "Піксель їсть корисну їжу 🥦",
    }

    effects = {
        "basic":   {"hunger": -20, "happiness": -5, "energy": 0},
        "treat":   {"hunger": -10, "happiness": +20, "energy": +5},
        "healthy": {"hunger": -30, "happiness": +5,  "energy": +10},
    }

    e = effects[request.food_type]
    _state.hunger = max(0, min(100, _state.hunger + e["hunger"]))
    _state.happiness = max(0, min(100, _state.happiness + e["happiness"]))
    _state.energy = max(0, min(100, _state.energy + e["energy"]))
    _state.last_updated = datetime.now().isoformat()

    return ActionResponse(
        success=True,
        message=messages[request.food_type],
        state=_to_response(_state),
    )


@router.post("/play", response_model=ActionResponse, summary="Пограти з тамагочі")
def play(request: PlayRequest):
    """
    **POST /play** — грає з тамагочі.
    
    Активності:
    - `ball` — гра з м'ячем (+15 щастя, -10 енергія)
    - `puzzle` — головоломка (+25 щастя, -20 енергія, +5 голод)
    - `dance` — танці (+20 щастя, -15 енергія, +10 голод)
    """
    _check_alive(_state)

    if _state.energy < 10:
        raise HTTPException(
            status_code=400,
            detail="Тамагочі надто втомлений для гри! Дай йому відпочити 😴"
        )

    valid_activities = ["ball", "puzzle", "dance"]
    if request.activity not in valid_activities:
        raise HTTPException(
            status_code=422,
            detail=f"Невідома активність '{request.activity}'. Доступні: {valid_activities}"
        )

    messages = {
        "ball":   "Піксель весело грає з м'ячиком! ⚽",
        "puzzle": "Піксель розгадує головоломку 🧩",
        "dance":  "Піксель танцює! 💃",
    }

    effects = {
        "ball":   {"happiness": +15, "energy": -10, "hunger": 0},
        "puzzle": {"happiness": +25, "energy": -20, "hunger": +5},
        "dance":  {"happiness": +20, "energy": -15, "hunger": +10},
    }

    e = effects[request.activity]
    _state.happiness = max(0, min(100, _state.happiness + e["happiness"]))
    _state.energy = max(0, min(100, _state.energy + e["energy"]))
    _state.hunger = max(0, min(100, _state.hunger + e["hunger"]))
    _state.last_updated = datetime.now().isoformat()

    return ActionResponse(
        success=True,
        message=messages[request.activity],
        state=_to_response(_state),
    )


@router.post("/sleep", response_model=ActionResponse, summary="Покласти тамагочі спати")
def sleep():
    """
    **POST /sleep** — тамагочі відпочиває.
    
    Відновлює енергію (+40), трохи збільшує голод (+10).
    """
    _check_alive(_state)

    _state.energy = min(100, _state.energy + 40)
    _state.hunger = min(100, _state.hunger + 10)
    _state.last_updated = datetime.now().isoformat()

    return ActionResponse(
        success=True,
        message="Піксель солодко спить 💤",
        state=_to_response(_state),
    )


@router.delete("/reset", response_model=ActionResponse, summary="Скинути стан тамагочі")
def reset():
    """
    **DELETE /reset** — скидає тамагочі до початкового стану.
    
    Використовується, якщо тамагочі загинув або для нового старту.
    """
    global _state
    _state = TamagotchiState()
    _state.last_updated = datetime.now().isoformat()

    return ActionResponse(
        success=True,
        message="Тамагочі відроджений! Зустрічай Пікселя! 🐣",
        state=_to_response(_state),
    )