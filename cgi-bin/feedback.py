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
print("<h2>100～119番目のレコード</h2>")
place_A = log[100:120]
print(place_A.to_html())

# place_Aの視線データの抽出
eye_A = place_A.loc[:, ["focus_x", "focus_y"]]
plt.figure()
eye_A.plot.scatter(x="focus_x", y="focus_y")
plt.savefig("fig/graph_A.png")
plt.close("all")

# place_Aのグラフを出力
print("<div style='text-align:center'>")
print("<img src=" + "'../fig/graph_A.png'" + " >")
print("</div>")

print("<h2>X座標が7300以上かつ7350以下のレコード</h2>")
place_B = log[(log.x >= 7300) & (log.x <= 7350)]
print(place_B.to_html())

# place_Bの視線データの抽出
eye_B = place_B.loc[:, ["focus_x", "focus_y"]]
plt.figure()
eye_B.plot.scatter(x="focus_x", y="focus_y")
plt.savefig("fig/graph_B.png")
plt.close("all")

# place_Bのグラフを出力
print("<div style='text-align:center'>")
print("<img src=" + "'../fig/graph_B.png'" + " >")
print("</div>")

print("</body>")
print("</html>")
