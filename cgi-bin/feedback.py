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

# place_Aスピードのデータ分析
place_A = log[(log.x >=6907) &(log.x <=7021)]
speed_A = place_A.loc[:, ["speed"]]
a= speed_A.mean() #speed平均値
print(a)
print("<br>")

#place_A視線平均
e_A = place_A.loc[:, ["focus"]]
print(e_A.mean())

# place_Aの視線データの抽出
eye_A = place_A.loc[:, ["focus_x", "focus_y"]]
plt.figure()
eye_A.plot.scatter(x="focus_x", y="focus_y")
plt.title('eyeA')
plt.savefig("fig/graph_A.png")
plt.close("all")

# plase_Aのスピードデータ抽出
spe_A = place_A.loc[:, ["x", "speed"]]
plt.figure()
spe_A.plot(x="x", y="speed")
plt.title('speedA')
plt.savefig("fig/graph_A1.png")
plt.close("all")


# place_Bの視線データの抽出
place_B = log[(log.x >= 7071) & (log.x <= 7250)]
eye_B = place_B.loc[:, ["focus_x", "focus_y"]]
plt.figure()
eye_B.plot.scatter(x="focus_x", y="focus_y")
plt.title('eyeB')
plt.savefig("fig/graph_B.png")
plt.close("all")

#データの出力
print(log.to_html())


# place_Aのグラフを出力
print("<div style='position:relative;top:-23600px;left:1000px;'>")
print("<h2>一つ目の交差点</h2>")
print("<table>")
print("<tr>")
print("<td><img src=" + "'../fig/graph_A.png'" + " ></td>")
print("<td><img src=" + "'../fig/graph_A1.png'" + " ></td>")
print("</tr>")
print("</table>")

# place_Bのグラフを出力
print("<table>")
print("<h2>二つ目の交差点</h2>")
print("<tr>")
print("<td><img src=" + "'../fig/graph_B.png'" + " width='700' height='500' ></td>")
print("</tr>")
print("</table>")
print("</div>")

print("</body>")
print("</html>")
