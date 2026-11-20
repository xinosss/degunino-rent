import os
import json
import time
import requests
import telebot
from telebot import types
from registry_data import load_flats, save_flats, calculate_score

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "bot_config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"token": "", "subscribers": [], "user_favorites": {}}

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def start_bot():
    cfg = load_config()
    token = cfg.get("token", "").strip()
    if not token or token == "YOUR_TELEGRAM_BOT_TOKEN":
        print("[TG BOT] Токен не настроен. Укажите токен бота в bot_config.json или через интерфейс.")
        return

    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start', 'help'])
    def cmd_start(msg):
        chat_id = msg.chat.id
        if chat_id not in cfg["subscribers"]:
            cfg["subscribers"].append(chat_id)
            save_config(cfg)

        text = (
            "🏠 *Бот уведомлений: Аренда в Дегунино (Циан)*\n\n"
            "Вы успешно подписаны на уведомления! 🚀\n\n"
            "• 🔔 *Новые квартиры* по вашим фильтрам (1-комн., до 70к, до 15 мин пешком, стиралка);\n"
            "• ⚠️ *Снятие избранных объявлений* или изменение цены;\n\n"
            "Команды:\n"
            "/top — Топ 5 лучших вариантов прямо сейчас\n"
            "/fav — Посмотреть избранные квартиры\n"
            "/link — Ссылка на интерактивный дашборд"
        )
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("🏆 Топ варианты", "❤️ Мое избранное")
        markup.row("🌐 Открыть дашборд", "🔍 Циан поиск")
        bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)

    @bot.message_handler(commands=['top'])
    @bot.message_handler(func=lambda m: m.text == "🏆 Топ варианты")
    def cmd_top(msg):
        flats = load_flats()
        flats.sort(key=lambda x: x.get("score", 0), reverse=True)
        top5 = flats[:5]
        
        bot.send_message(msg.chat.id, "🔍 *Топ лучших вариантов в Дегунино:*", parse_mode="Markdown")
        for f in top5:
            card = (
                f"🌟 *{f['title']}* — *{f['price']:,} ₽/мес*\n"
                f"📍 {f['district']}, {f['address']}\n"
                f"🚇 {f['metro']} — *{f['metro_time']} мин пешком*\n"
                f"🧺 Стиралка: Есть | Ремонт: {f['repair']}\n"
                f"💰 {'Без комиссии (0%)' if f['commission'] == 0 else f'Комиссия {f["commission"]}%'}\n"
                f"🏆 Рейтинг: *{f.get('score', 0)}/100*\n"
            )
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("🔗 На Циан", url=f["url"]),
                types.InlineKeyboardButton("⭐ В избранное", callback_data=f"fav_{f['id']}")
            )
            bot.send_message(msg.chat.id, card, parse_mode="Markdown", reply_markup=markup)

    @bot.message_handler(commands=['fav'])
    @bot.message_handler(func=lambda m: m.text == "❤️ Мое избранное")
    def cmd_fav(msg):
        chat_id = str(msg.chat.id)
        fav_ids = cfg.get("user_favorites", {}).get(chat_id, [])
        if not fav_ids:
            bot.send_message(msg.chat.id, "У вас пока нет сохраненных квартир в избранном бота.")
            return

        flats = {f["id"]: f for f in load_flats()}
        bot.send_message(msg.chat.id, f"❤️ *Ваше избранное ({len(fav_ids)}):*", parse_mode="Markdown")
        for fid in fav_ids:
            if fid in flats:
                f = flats[fid]
                card = (
                    f"⭐ *{f['title']}* — *{f['price']:,} ₽*\n"
                    f"📍 {f['address']} (м. {f['metro']}, {f['metro_time']} мин)\n"
                )
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("🔗 Открыть на Циан", url=f["url"]))
                bot.send_message(msg.chat.id, card, parse_mode="Markdown", reply_markup=markup)

    @bot.message_handler(commands=['link'])
    @bot.message_handler(func=lambda m: m.text == "🌐 Открыть дашборд")
    def cmd_link(msg):
        pub_url = cfg.get("public_url", "http://localhost:8080")
        bot.send_message(
            msg.chat.id,
            f"📱 *Интерактивный дашборд со всеми фильтрами:*\n{pub_url}",
            parse_mode="Markdown"
        )

    @bot.message_handler(func=lambda m: m.text == "🔍 Циан поиск")
    def cmd_cian(msg):
        cian_url = "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&room1=1&rayon[0]=337&rayon[1]=357&maxprice=70000&foot_min=15&only_foot=2"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Перейти в выдачу Циан", url=cian_url))
        bot.send_message(msg.chat.id, "Прямая выдача поиска Циан по всем заданным фильтрам:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("fav_"))
    def handle_fav_callback(call):
        chat_id = str(call.message.chat.id)
        fid = call.data.replace("fav_", "")
        if "user_favorites" not in cfg:
            cfg["user_favorites"] = {}
        if chat_id not in cfg["user_favorites"]:
            cfg["user_favorites"][chat_id] = []
        
        if fid not in cfg["user_favorites"][chat_id]:
            cfg["user_favorites"][chat_id].append(fid)
            save_config(cfg)
            bot.answer_callback_query(call.id, "Добавлено в избранное! Вы получите уведомление, если объявление снимут.")
        else:
            bot.answer_callback_query(call.id, "Уже в вашем избранном.")

    print(f"[TG BOT] Бот запущен! Имя бота: @{bot.get_me().username}")
    bot.infinity_polling()

def send_telegram_alert(message, markup=None):
    cfg = load_config()
    token = cfg.get("token", "").strip()
    if not token or token == "YOUR_TELEGRAM_BOT_TOKEN":
        return
    bot = telebot.TeleBot(token)
    for chat_id in cfg.get("subscribers", []):
        try:
            bot.send_message(chat_id, message, parse_mode="Markdown", reply_markup=markup)
        except Exception as e:
            print(f"[TG BOT] Ошибка отправки в {chat_id}: {e}")

if __name__ == "__main__":
    start_bot()
