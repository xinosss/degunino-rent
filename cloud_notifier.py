import requests
import os
import json

def run():
    token = os.environ.get("TELEGRAM_TOKEN", "9271631223:AAGaJ8w9kbFIdaT8G3rMgMMdvD5tdlFQaLA")
    print("Requesting getUpdates...")
    try:
        res = requests.get(f"https://api.telegram.org/bot{token}/getUpdates?offset=-10", timeout=15).json()
    except Exception as e:
        print("Telegram API request error:", e)
        return

    print("Updates result:", json.dumps(res, ensure_ascii=False))

    chat_ids = set()
    if "result" in res and isinstance(res["result"], list):
        for item in res["result"]:
            msg = item.get("message") or item.get("callback_query", {}).get("message") or item.get("my_chat_member")
            if msg and "chat" in msg:
                chat_ids.add(msg["chat"]["id"])
            elif "channel_post" in item:
                chat_ids.add(item["channel_post"]["chat"]["id"])

    print(f"Detected chat IDs: {chat_ids}")

    if not chat_ids:
        print("No chat IDs found. Please send a message to the bot first.")
        return

    # Загружаем квартиры
    flats_file = os.path.join(os.path.dirname(__file__), "flats_data.json")
    with open(flats_file, "r", encoding="utf-8") as f:
        flats = json.load(f)

    flats.sort(key=lambda x: x.get("score", 0), reverse=True)
    top = flats[0] if flats else None

    for cid in chat_ids:
        comm_str = "0% Без комиссии" if top["commission"] == 0 else f"Комиссия {top['commission']}%"
        text = (
            "🏠 *Реестр квартир Дегунино (Циан) подключен!*\n\n"
            "Вы успешно получаете уведомления по вашим критериям:\n"
            "• 1-комн. квартиры до 70 000 ₽/мес\n"
            "• Пешком до метро ≤ 15 минут\n"
            "• Со стиральной машиной\n\n"
            f"🌟 *Лучший вариант сейчас:*\n"
            f"*{top['title']}* — *{top['price']:,} ₽/мес*\n"
            f"📍 {top['address']} (м. {top['metro']}, 🚶 {top['metro_time']} мин)\n"
            f"💰 {comm_str}\n\n"
            "📱 *Интерактивный реестр квартир:*\nhttps://xinosss.github.io/degunino-rent/"
        )
        payload = {
            "chat_id": cid,
            "text": text,
            "parse_mode": "Markdown",
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": "🌐 Открыть Реестр", "url": "https://xinosss.github.io/degunino-rent/"}],
                    [{"text": "🔗 Открыть на Циан", "url": top["url"]}]
                ]
            }
        }
        r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json=payload, timeout=15)
        print(f"Sent to {cid}: {r.status_code} {r.text}")

if __name__ == "__main__":
    run()
