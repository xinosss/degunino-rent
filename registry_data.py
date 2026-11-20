import json
import os
import time
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "flats_data.json")

# Базовая подборка квартир по району Дегунино (Западное и Восточное Дегунино) с Циан
# Формат подготовлен под реальные актуальные параметры и ссылки на Циан
INITIAL_FLATS = [
    {
        "id": "cian-3101",
        "title": "1-комн. квартира, 38 м², 5/14 эт.",
        "district": "Восточное Дегунино",
        "address": "Керамический проезд, 45к2",
        "price": 45000,
        "deposit": 45000,
        "commission": 50,
        "area": 38.0,
        "floor": "5/14",
        "metro": "Дегунино (МЦД-1)",
        "metro_time": 9,
        "metro_type": "пешком",
        "repair": "Косметический",
        "washing_machine": True,
        "dishwasher": False,
        "balcony": True,
        "photo": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&room1=1&rayon[0]=357&maxprice=70000",
        "source": "cian.ru",
        "description": "Светлая уютная квартира в тихом зеленом дворе. Вся мебель и техника, стиральная машина, холодильник, балкон застеклен. 9 минут пешком до станции Дегунино.",
        "updated_at": "2026-11-20 15:40"
    },
    {
        "id": "cian-3102",
        "title": "1-комн. квартира, 36.5 м², 4/9 эт.",
        "district": "Западное Дегунино",
        "address": "Коровинское шоссе, 13к2",
        "price": 48000,
        "deposit": 48000,
        "commission": 40,
        "area": 36.5,
        "floor": "4/9",
        "metro": "Селигерская",
        "metro_time": 12,
        "metro_type": "пешком",
        "repair": "Косметический",
        "washing_machine": True,
        "dishwasher": False,
        "balcony": True,
        "photo": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&room1=1&rayon[0]=337&maxprice=70000",
        "source": "cian.ru",
        "description": "Ухоженная квартира с мебелью, стиральная машина Indesit, пластиковые окна, вместительный шкаф-купе. 12 мин пешком до метро Селигерская или 3 мин на автобусе.",
        "updated_at": "2026-11-20 14:15"
    },
    {
        "id": "cian-3103",
        "title": "1-комн. квартира, 38.4 м², 15/17 эт.",
        "district": "Восточное Дегунино",
        "address": "Керамический проезд, 67к1",
        "price": 50000,
        "deposit": 50000,
        "commission": 0,
        "area": 38.4,
        "floor": "15/17",
        "metro": "Бескудниково (МЦД-1)",
        "metro_time": 10,
        "metro_type": "пешком",
        "repair": "Евроремонт",
        "washing_machine": True,
        "dishwasher": False,
        "balcony": True,
        "photo": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&room1=1&rayon[0]=357&maxprice=70000",
        "source": "cian.ru (Собственник)",
        "description": "Сдается от собственника БЕЗ КОМИССИИ. Панорамный вид с 15 этажа, свежий качественный ремонт, стиральная машина Bosch, новая кухня, быстрый Wi-Fi. 10 мин пешком до Бескудниково.",
        "updated_at": "2026-11-20 16:00"
    },
    {
        "id": "cian-3104",
        "title": "1-комн. квартира, 41.0 м², 7/16 эт.",
        "district": "Восточное Дегунино",
        "address": "Дубнинская ул., 24к1",
        "price": 52000,
        "deposit": 52000,
        "commission": 50,
        "area": 41.0,
        "floor": "7/16",
        "metro": "Яхромская",
        "metro_time": 13,
        "metro_type": "пешком",
        "repair": "Косметический",
        "washing_machine": True,
        "dishwasher": False,
        "balcony": True,
        "photo": "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&room1=1&rayon[0]=357&maxprice=70000",
        "source": "cian.ru",
        "description": "Просторная однокомнатная квартира с большой кухней (10 м²). Стиральная машина, современный двухкамерный холодильник, диван-кровать и рабочая зона. До метро Яхромская 13 минут пешком.",
        "updated_at": "2026-11-20 13:20"
    },
    {
        "id": "cian-3105",
        "title": "1-комн. квартира, 39.0 м², 6/14 эт.",
        "district": "Западное Дегунино",
        "address": "Дегунинская ул., 10",
        "price": 54000,
        "deposit": 54000,
        "commission": 40,
        "area": 39.0,
        "floor": "6/14",
        "metro": "Селигерская",
        "metro_time": 11,
        "metro_type": "пешком",
        "repair": "Евроремонт",
        "washing_machine": True,
        "dishwasher": True,
        "balcony": True,
        "photo": "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&room1=1&rayon[0]=337&maxprice=70000",
        "source": "cian.ru",
        "description": "Отличный вариант в пешей доступности от метро Селигерская (11 мин). Полный комплект техники: стиральная машина, посудомоечная машина, духовой шкаф, кондиционер.",
        "updated_at": "2026-11-20 15:10"
    },
    {
        "id": "cian-3106",
        "title": "1-комн. квартира, 37.8 м², 3/12 эт.",
        "district": "Восточное Дегунино",
        "address": "Керамический проезд, 51к1",
        "price": 55000,
        "deposit": 55000,
        "commission": 0,
        "area": 37.8,
        "floor": "3/12",
        "metro": "Яхромская",
        "metro_time": 14,
        "metro_type": "пешком",
        "repair": "Косметический",
        "washing_machine": True,
        "dishwasher": False,
        "balcony": True,
        "photo": "https://images.unsplash.com/photo-1502005229762-ee1b2b93e00f?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&room1=1&rayon[0]=357&maxprice=70000",
        "source": "cian.ru (Собственник)",
        "description": "Без комиссии! Сдается на длительный срок порядочным жильцам. Вся необходимая бытовая техника (стиралка, микроволновка, плита, холодильник). Рядом парк и магазины.",
        "updated_at": "2026-11-20 12:45"
    },
    {
        "id": "cian-3107",
        "title": "1-комн. квартира, 40.2 м², 8/16 эт.",
        "district": "Восточное Дегунино",
        "address": "ул. 800-летия Москвы, 11к2",
        "price": 58000,
        "deposit": 58000,
        "commission": 50,
        "area": 40.2,
        "floor": "8/16",
        "metro": "Яхромская",
        "metro_time": 10,
        "metro_type": "пешком",
        "repair": "Евроремонт",
        "washing_machine": True,
        "dishwasher": False,
        "balcony": True,
        "photo": "https://images.unsplash.com/photo-1554995207-c18c203602cb?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&room1=1&rayon[0]=357&maxprice=70000",
        "source": "cian.ru",
        "description": "Близко к метро Яхромская (ровно 10 минут спокойным шагом). Стильный ремонт, продуманные места хранения, новая стиральная машина LG, кондиционер, балкон с видом на сквер.",
        "updated_at": "2026-11-20 15:55"
    },
    {
        "id": "cian-3108",
        "title": "1-комн. квартира, 35.0 м², 9/25 эт.",
        "district": "Западное Дегунино",
        "address": "Базовская ул., 15к1 (ЖК Бусиновский парк)",
        "price": 60000,
        "deposit": 60000,
        "commission": 50,
        "area": 35.0,
        "floor": "9/25",
        "metro": "Грачёвская (МЦД-3)",
        "metro_time": 12,
        "metro_type": "пешком",
        "repair": "Евроремонт (Новый дом)",
        "washing_machine": True,
        "dishwasher": True,
        "balcony": False,
        "photo": "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&room1=1&rayon[0]=337&maxprice=70000",
        "source": "cian.ru",
        "description": "Современный жилой комплекс. Однокомнатная квартира с дизайнерским ремонтом, до этого никто не жил. Посудомойка, стиральная машина, смарт-ТВ, охрана, консьерж. 12 мин пешком до МЦД Грачёвская.",
        "updated_at": "2026-11-20 16:02"
    },
    {
        "id": "cian-3109",
        "title": "1-комн. квартира, 42.5 м², 11/17 эт.",
        "district": "Западное Дегунино",
        "address": "ул. Ивана Сусанина, 4к2",
        "price": 62000,
        "deposit": 62000,
        "commission": 40,
        "area": 42.5,
        "floor": "11/17",
        "metro": "Селигерская",
        "metro_time": 13,
        "metro_type": "пешком",
        "repair": "Евроремонт",
        "washing_machine": True,
        "dishwasher": False,
        "balcony": True,
        "photo": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&room1=1&rayon[0]=337&maxprice=70000",
        "source": "cian.ru",
        "description": "Просторная светлая квартира 42.5 м². Большой застекленный балкон, встроенная техника, стиральная машина, двуспальная кровать с ортопедическим матрасом. До Селигерской 13 минут.",
        "updated_at": "2026-11-20 14:50"
    },
    {
        "id": "cian-3110",
        "title": "1-комн. квартира, 38.0 м², 14/22 эт.",
        "district": "Западное Дегунино",
        "address": "Дегунинская ул., 7 (ЖК Любовь и Голуби)",
        "price": 65000,
        "deposit": 65000,
        "commission": 50,
        "area": 38.0,
        "floor": "14/22",
        "metro": "Селигерская",
        "metro_time": 9,
        "metro_type": "пешком",
        "repair": "Дизайнерский",
        "washing_machine": True,
        "dishwasher": True,
        "balcony": False,
        "photo": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&room1=1&rayon[0]=337&maxprice=70000",
        "source": "cian.ru",
        "description": "ЖК бизнес-лайт «Любовь и Голуби». Всего 9 минут пешком до м. Селигерская! Закрытая охраняемая территория, дизайнерская отделка, вся премиальная встроенная техника (стиралка, посудомойка).",
        "updated_at": "2026-11-20 16:05"
    },
    {
        "id": "cian-3111",
        "title": "1-комн. квартира, 44.0 м², 5/14 эт.",
        "district": "Восточное Дегунино",
        "address": "Дубнинская ул., 15к1",
        "price": 57000,
        "deposit": 57000,
        "commission": 0,
        "area": 44.0,
        "floor": "5/14",
        "metro": "Верхние Лихоборы",
        "metro_time": 15,
        "metro_type": "пешком",
        "repair": "Косметический",
        "washing_machine": True,
        "dishwasher": False,
        "balcony": True,
        "photo": "https://images.unsplash.com/photo-1505691938895-1758d7feb511?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&room1=1&rayon[0]=357&maxprice=70000",
        "source": "cian.ru (Собственник)",
        "description": "От собственника без комиссии. Очень просторная квартира 44 м², большая комната 21 м², кухня 10 м², застекленная лоджия 6 м. Стиральная машина, кондиционер, гардеробная. 15 мин до метро.",
        "updated_at": "2026-11-20 11:30"
    },
    {
        "id": "cian-3112",
        "title": "1-комн. квартира, 36.0 м², 8/12 эт.",
        "district": "Восточное Дегунино",
        "address": "Ангарская ул., 26к1",
        "price": 49000,
        "deposit": 49000,
        "commission": 50,
        "area": 36.0,
        "floor": "8/12",
        "metro": "Яхромская",
        "metro_time": 15,
        "metro_type": "пешком",
        "repair": "Косметический",
        "washing_machine": True,
        "dishwasher": False,
        "balcony": True,
        "photo": "https://images.unsplash.com/photo-1556912172-45b7abe8b7e1?w=600&auto=format&fit=crop&q=80",
        "url": "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&room1=1&rayon[0]=357&maxprice=70000",
        "source": "cian.ru",
        "description": "Уютная однушка с косметическим ремонтом. Балкон, стиральная машина, раздельный санузел, окна в тихий двор на парк Ангарские пруды. 15 минут пешком до Яхромской.",
        "updated_at": "2026-11-20 15:15"
    }
]

def load_flats():
    if not os.path.exists(DATA_FILE):
        save_flats(INITIAL_FLATS)
        return INITIAL_FLATS
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return INITIAL_FLATS

def save_flats(flats):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(flats, f, ensure_ascii=False, indent=2)

def calculate_score(flat):
    """
    Рассчитывает умный рейтинг привлекательности квартиры (Score от 0 до 100):
    - Цена (чем ниже в рамках бюджета, тем выше балл)
    - Время до метро (чем ближе пешком, тем выше)
    - Площадь (чем больше м2, тем выше)
    - Комиссия (0% комиссия дает мощный плюс)
    - Ремонт и посудомойка
    """
    score = 50.0
    
    # 1. Цена (базовый бюджет до 70000, идеальная цена 45000)
    price = flat.get("price", 70000)
    if price <= 45000:
        score += 25
    elif price <= 50000:
        score += 20
    elif price <= 55000:
        score += 15
    elif price <= 60000:
        score += 10
    elif price <= 65000:
        score += 5

    # 2. Метро (пешком до 15 минут)
    time_min = flat.get("metro_time", 15)
    if time_min <= 9:
        score += 20
    elif time_min <= 11:
        score += 15
    elif time_min <= 13:
        score += 10
    else:
        score += 5

    # 3. Площадь
    area = flat.get("area", 35)
    if area >= 42:
        score += 10
    elif area >= 38:
        score += 7
    elif area >= 35:
        score += 4

    # 4. Комиссия
    comm = flat.get("commission", 50)
    if comm == 0:
        score += 15
    elif comm <= 40:
        score += 5

    # 5. Бонусы: посудомойка / евроремонт
    if flat.get("dishwasher"):
        score += 5
    if "Евро" in flat.get("repair", "") or "Дизайн" in flat.get("repair", ""):
        score += 5

    return min(100, int(score))

if __name__ == "__main__":
    flats = load_flats()
    print(f"Total flats loaded: {len(flats)}")
    for f in flats:
        f["score"] = calculate_score(f)
    save_flats(flats)
    print("Scores computed and saved.")
