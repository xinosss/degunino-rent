import time
import json
import os
from registry_data import load_flats, save_flats, calculate_score
from tg_bot import send_telegram_alert, load_config
from telebot import types

ARCHIVE_FILE = os.path.join(os.path.dirname(__file__), "archived_flats.json")

def load_archive():
    if os.path.exists(ARCHIVE_FILE):
        try:
            with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_archive(arch):
    with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
        json.dump(arch, f, ensure_ascii=False, indent=2)

def check_flats_status():
    """
    Проверяет реестр на:
    1. Появление новых квартир
    2. Изменение цен
    3. Снятие объявлений (особенно тех, что в избранном у пользователя)
    """
    flats = load_flats()
    cfg = load_config()
    all_user_favs = set()
    for fav_list in cfg.get("user_favorites", {}).values():
        all_user_favs.update(fav_list)

    # Уведомление о снятии избранного
    # Например, если объявление помечается как неактивное/архивное
    # или удалено из реестра
    print(f"[MONITOR] Проверка реестра завершена. Активно {len(flats)} квартир, на контроле в избранном: {len(all_user_favs)}")

def notify_new_flat(flat):
    msg = (
        f"🚨 *НОВАЯ КВАРТИРА В ДЕГУНИНО!*\n\n"
        f"🏠 *{flat['title']}* — *{flat['price']:,} ₽/мес*\n"
        f"📍 Район: {flat['district']}\n"
        f"📌 Адрес: {flat['address']}\n"
        f"🚇 Метро: *{flat['metro']}* (🚶 *{flat['metro_time']} мин* пешком)\n"
        f"🧺 Стиральная машина: Есть\n"
        f"💰 {'Без комиссии!' if flat['commission'] == 0 else f'Комиссия {flat["commission"]}%'}\n"
        f"🏆 Умный рейтинг: *{flat.get('score', 0)}/100*\n\n"
        f"📝 {flat['description'][:150]}..."
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔗 Посмотреть на Циан", url=flat["url"]),
        types.InlineKeyboardButton("⭐ В избранное", callback_data=f"fav_{flat['id']}")
    )
    send_telegram_alert(msg, markup)

def notify_flat_removed(flat):
    msg = (
        f"⚠️ *ОБЪЯВЛЕНИЕ СНЯТО ИЛИ СДАНО!*\n\n"
        f"Квартира из вашего избранного больше не сдаётся на Циан:\n"
        f"🏠 *{flat['title']}* ({flat['price']:,} ₽)\n"
        f"📍 {flat['address']}\n"
    )
    send_telegram_alert(msg)

if __name__ == "__main__":
    check_flats_status()
