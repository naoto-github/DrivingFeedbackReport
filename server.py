from http.server import HTTPServer, CGIHTTPRequestHandler

class Handler(CGIHTTPRequestHandler):
    # CGIを設置するディレクトリ
    cgi_directories = ["/cgi-bin"]

# ポート番号
PORT = 8080

# IPアドレス
HOST = "127.0.0.1"

# URLを表示
print("http://127.0.0.1:8080/cgi-bin/feedback.py")

# サーバの起動
httpd = HTTPServer((HOST, PORT), Handler)
httpd.serve_forever()
