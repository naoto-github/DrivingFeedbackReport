import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# CSVファイルの読込
log = pd.read_csv("data/kodera-log1.csv", sep=",") # 古寺 1回目
#log = pd.read_csv("data/kodera-log2.csv", sep=",") # 古寺 2回目
#log = pd.read_csv("data/imai-log1.csv", sep=",")  # 今井 1回目
#log = pd.read_csv("data/imai-log2.csv", sep=",") # 今井 2回目

# Pandasの設定
pd.set_option("display.max_rows", None)

# 視線データと速度データの抽出
def getData(start_x, end_x):
    place = log[(log.x >= start_x) &(log.x <= end_x)]
    eye_data = place.loc[:, ["focus_x", "focus_y"]]
    speed_data = place.loc[:, ["x", "speed"]]
    focus_data = place.loc[:, ["x", "focus"]]

    # Y座標の変換
    eye_max = eye_data.max()
    eye_data = eye_max - eye_data

    return (eye_data, speed_data, focus_data)

# 視線データのグラフ化
def makeEyeGraph(eye_data, file_name):
    plt.figure()
    eye_data.plot.scatter(x="focus_x", y="focus_y", xlim=[0, 1920], ylim=[0, 1080])
    plt.xlabel("X[px]")
    plt.ylabel("Y[px]")
    plt.title("Eye Moving")
    plt.savefig("fig/" + file_name)
    plt.close("all")

# 速度データのグラフ化
def makeSpeedGraph(speed_data, file_name):
    plt.figure()
    speed_data.plot(x="x", y="speed")
    plt.xlabel("Distance[km]")
    plt.ylabel("Speed[km/h]")
    plt.title("Speed")
    plt.savefig("fig/" + file_name)
    plt.close("all")

# 統計量の表示
def showStat(eye_data, speed_data):

    # 視線統計量
    eye_mean = eye_data.mean()
    eye_std = eye_data.std()
    eye_max = eye_data.max()
    eye_min = eye_data.min()

    print("<div>")
    print("<h4>視線 統計量</h4>")
    print("<table border='1' style='border-collapse: collapse'>")
    print(f"<tr><th>平均<th> <td>X:{round(eye_mean[0], 2)}[px] Y:{round(eye_mean[1], 2)}[px]</td></tr>")
    print(f"<tr><th>標準偏差<th> <td>X:{round(eye_std[0], 2)}[px] Y:{round(eye_std[1], 2)}[px]</td></tr>")
    print(f"<tr><th>最大値<th> <td>X:{round(eye_max[0], 2)}[px] Y:{round(eye_max[1], 2)}[px]</td></tr>")
    print(f"<tr><th>最小値<th> <td>X:{round(eye_min[0], 2)}[px] Y:{round(eye_min[1], 2)}[px]</td></tr>")
    print("</table>")

    # 速度統計量
    speed_mean = speed_data.mean()[1]
    speed_std = speed_data.std()[1]
    speed_max = speed_data.max()[1]
    speed_min = speed_data.min()[1]

    print("<h4>速度 統計量</h4>")
    print("<table border='1' style='border-collapse: collapse'>")
    print(f"<tr><th>平均<th> <td>{round(speed_mean, 2)}[km/h]</td></tr>")
    print(f"<tr><th>標準偏差<th> <td>{round(speed_std, 2)}[km/h]</td></tr>")
    print(f"<tr><th>最大値<th> <td>{round(speed_max, 2)}[km/h]</td></tr>")
    print(f"<tr><th>最小値<th> <td>{round(speed_min, 2)}[km/h]</td></tr>")
    print("</table>")

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
print("<title>運転結果 フィードバック・レポート</title>")
print("</head>")

print("<body>")
print("<h1>運転結果 フィードバック・レポート</h1>");

# 第１交差点
print("<h2>第１交差点</h2>")
target_x = 6964
distance = 50
eye_data, speed_data, focus_data = getData(target_x - distance, target_x + distance)
makeEyeGraph(eye_data, "eye-1.png")
makeSpeedGraph(speed_data, "speed-1.png")
showStat(eye_data, speed_data)
plotGraph("eye-1.png", "speed-1.png")

#print(eye_data.to_html())
#print(focus_data.to_html())

# 第２交差点
print("<h2>第２交差点</h2>")
target_x = 7160
distance = 50
eye_data, speed_data, focus_data = getData(target_x - distance, target_x + distance)
makeEyeGraph(eye_data, "eye-2.png")
makeSpeedGraph(speed_data, "speed-2.png")
showStat(eye_data, speed_data)
plotGraph("eye-2.png", "speed-2.png")

#print(eye_data.to_html())
#print(focus_data.to_html())

# 全データの表示
#print(log.to_html())

print("</body>")
print("</html>")
