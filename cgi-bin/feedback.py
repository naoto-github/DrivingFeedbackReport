import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# CSVファイルの読込
log = pd.read_csv("data/mukai-log.csv", sep=",")
pd.set_option("display.max_rows", None)

print ("Content-type:text/html\n\n")
print("<!DOCTYPE html>")
print("<html>")

print("<head>")
print("<meta charset='utf-8'>")
print("<title>運転結果</title>")
print("</head>")

print("<body>")
print("<h1>運転結果</h1>");

# CSVデータのHTML出力
print(log.to_html())

# 視線データの抽出
eye = log.loc[:, ["focus_x", "focus_y"]]
#print(eye.to_html())

# 視線データをグラフ化
plt.figure()
eye.plot.scatter(x="focus_x", y="focus_y")
plt.savefig("fig/graph.png")
plt.close("all")

# グラフのHTML出力
print("<div>")
print("<img src=" + "'../fig/graph.png'" + " >")
print("</div>")

print("</body>")
print("</html>")
