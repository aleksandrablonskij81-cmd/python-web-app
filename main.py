import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Кастомный обработчик HTTP-запросов"""

    def do_GET(self):
        """Обработка GET-запросов"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        routes = {
            '/': 'templates/index.html',
            '/index': 'templates/index.html',
            '/categories': 'templates/categories.html',
            '/orders': 'templates/orders.html',
            '/contacts': 'templates/contacts.html',
        }

        if path in routes:
            self.send_html_response(routes[path])
        else:
            self.send_html_response('templates/404.html', status=404)

    def do_POST(self):
        """Обработка POST-запросов"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/contacts':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')

            params = parse_qs(post_data)
            name = params.get('name', [''])[0]
            email = params.get('email', [''])[0]
            message = params.get('message', [''])[0]

            print("\n" + "=" * 50)
            print("📨 ПОЛУЧЕНО НОВОЕ СООБЩЕНИЕ")
            print(f"👤 Имя: {name}")
            print(f"📧 Email: {email}")
            print(f"💬 Сообщение: {message}")
            print("=" * 50 + "\n")

            with open('templates/contacts.html', 'r', encoding='utf-8') as file:
                content = file.read()

            success_message = """
            <div class="alert alert-success alert-dismissible fade show mt-3" role="alert">
                <strong>Спасибо!</strong> Ваше сообщение отправлено.
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
            """
            content = content.replace('<form method="POST"',
                                      success_message + '<form method="POST"')

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            self.send_html_response('templates/404.html', status=404)

    def send_html_response(self, filepath, status=200):
        """Универсальный метод для отправки HTML-страницы"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            self.send_response(status)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))

        except FileNotFoundError:
            self.send_error(500, "Внутренняя ошибка: файл не найден")
        except Exception as e:
            self.send_error(500, f"Внутренняя ошибка: {str(e)}")


def run_server():
    """Запуск сервера"""
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Сервер запущен на http://localhost:{PORT}")
        print("📋 Доступные страницы:")
        print("   - http://localhost:8000/          (Главная)")
        print("   - http://localhost:8000/categories (Категории)")
        print("   - http://localhost:8000/orders    (Заказы)")
        print("   - http://localhost:8000/contacts  (Контакты)")
        print("⏹️  Нажми Ctrl+C для остановки\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Сервер остановлен")


if __name__ == "__main__":
    run_server()
