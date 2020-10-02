from http.server import HTTPServer, CGIHTTPRequestHandler
import argparse
import webbrowser

# 引数の処理
parser = argparse.ArgumentParser(description="Feedback Report for Drivers")
parser.add_argument("--log", help="LOG FILE", required="True")
args = parser.parse_args()

class Handler(CGIHTTPRequestHandler):
    # CGIを設置するディレクトリ
    cgi_directories = ["/cgi-bin"]

# ポート番号
PORT = 8080

# IPアドレス
HOST = "127.0.0.1"

# URLを表示
url_en = "http://127.0.0.1:8080/cgi-bin/feedback-en.py?log=" + args.log
url_ja = "http://127.0.0.1:8080/cgi-bin/feedback-ja.py?log=" + args.log
print(f"Please access following url.")
print(f"English Version: {url_en}")
print(f"Japanese Version: {url_ja}")

# 規定のブラウザで開く
webbrowser.open(url_en)

# サーバの起動
httpd = HTTPServer((HOST, PORT), Handler)
httpd.serve_forever()
