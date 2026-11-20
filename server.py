import os
import json
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
from registry_data import load_flats, save_flats, calculate_score

PORT = 8080

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/flats":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            flats = load_flats()
            self.wfile.write(json.dumps(flats, ensure_ascii=False).encode("utf-8"))
        elif parsed.path == "/" or parsed.path == "/index.html":
            self.path = "/index.html"
            return super().do_GET()
        else:
            return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/refresh":
            # Перерасчет рейтингов и обновление реестра
            flats = load_flats()
            for f in flats:
                f["score"] = calculate_score(f)
            save_flats(flats)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            response = {
                "status": "ok",
                "message": "Реестр обновлен",
                "flats": flats
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_error(404, "Not Found")

def run():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    local_ip = get_local_ip()
    print("="*60)
    print("   🏠 ИНТЕРАКТИВНЫЙ РЕЕСТР КВАРТИР (ДЕГУНИНО / ЦИАН)")
    print("="*60)
    print(f"-> Локально на компьютере: http://localhost:{PORT}")
    print(f"-> С ТЕЛЕФОНА (по той же сети Wi-Fi): http://{local_ip}:{PORT}")
    print("="*60)

    server = HTTPServer(("0.0.0.0", PORT), CustomHandler)
    server.serve_forever()

if __name__ == "__main__":
    run()
