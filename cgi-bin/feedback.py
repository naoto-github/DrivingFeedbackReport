import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# CSVファイルの読込
log = pd.read_csv("data/kodera-log.csv", sep=",")
#log = pd.read_csv("data/imai-log.csv", sep=",")
pd.set_option("display.max_rows", None)

# 視線データと速度データの抽出
def getData(start_x, end_x):
    place = log[(log.x >= start_x) &(log.x <= end_x)]
    eye_data = place.loc[:, ["focus_x", "focus_y"]]
    speed_data = place.loc[:, ["x", "speed"]]
    return (eye_data, speed_data)

# 視線データのグラフ化
def makeEyeGraph(eye_data, file_name):
    plt.figure()
    eye_data.plot.scatter(x="focus_x", y="focus_y")
    plt.title(file_name)
    plt.savefig("fig/" + file_name)
    plt.close("all")

# 速度データのグラフ化
def makeSpeedGraph(speed_data, file_name):
    plt.figure()
    speed_data.plot(x="x", y="speed")
    plt.title(file_name)
    plt.savefig("fig/" + file_name)
    plt.close("all")

# 統計量の表示
def showStat(eye_data, speed_data):
    print("<div>")
    print("<h4>視線 統計量</h4>")
    print(f"<p>平均 X:{round(eye_data.mean()[0], 2)} Y:{round(eye_data.mean()[1], 2)}")
    print(f"<p>標準偏差 X:{round(eye_data.std()[0], 2)} Y:{round(eye_data.std()[1], 2)}")
    print("<h4>速度 統計量</h4>")
    print(f"<p>平均 {speed_data.mean()[1]}")
    print(f"<p>標準偏差 {speed_data.std()[1]}")
    print("</div>")

# グラフの描画
def plotGraph(file_name1, file_name2):
    print("<div>")
    print("<table>")
    print("<tr>")
    print(f"<td><img src='../fig/{file_name1}'></td>")
    print(f"<td><img src='../fig/{file_name2}'></td>")
    print("</tr>")
    print("</table>")

print ("Content-type:text/html\n\n")
print("<!DOCTYPE html>")
print("<html>")

print("<head>")
print("<meta charset='utf-8'>")
print("<title>運転結果</title>")
print("</head>")

print("<body>")
print("<h1>運転結果</h1>");

# 第１交差点
print("<h2>第１交差点</h2>")
eye_data, speed_data = getData(6907, 7021)
makeEyeGraph(eye_data, "eye-1.png")
makeSpeedGraph(speed_data, "speed-1.png")
showStat(eye_data, speed_data)
plotGraph("eye-1.png", "speed-1.png")

# 第２交差点
print("<h2>第２交差点</h2>")
eye_data, speed_data = getData(7071, 7250)
makeEyeGraph(eye_data, "eye-2.png")
makeSpeedGraph(speed_data, "speed-2.png")
showStat(eye_data, speed_data)
plotGraph("eye-2.png", "speed-2.png")

# 全データの表示
# print(log.to_html())

print("</body>")
print("</html>")
