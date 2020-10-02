import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
import argparse

# 文字化けの解消
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding = 'utf-8')

# 引数の処理
parser = argparse.ArgumentParser(description="Feedback Report for Drivers")
parser.add_argument("--log", help="ログファイル", required=True)
args = parser.parse_args()

print(args.log)

# CSVファイルの読込
#log = pd.read_csv("data/kodera-log1.csv", sep=",") # 古寺 1回目
log = pd.read_csv("data/kodera-log2.csv", sep=",") # 古寺 2回目
#log = pd.read_csv("data/imai-log1.csv", sep=",")  # 今井 1回目
#log = pd.read_csv("data/imai-log2.csv", sep=",") # 今井 2回目

# Pandasの設定
pd.set_option("display.max_rows", None)

# 視線データと速度データの抽出
def getData(start_x, end_x):
    place = log[(log.x >= start_x) & (log.x <= end_x)]
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

eye1 = 0
eye2 = 0
s1 = 0
s2 = 0
s3 = 0
sum = 0
# 統計量の表示
def showStat1(eye_data, speed_data):
    global eye1
    global s1
    global sum

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
    print("<h4>評価 コメント</h4>")
    if eye_max[0] >= 1420 and eye_min[0] <= 500 :   #左右を確認した
        eye1 = 8
        print("左右確認はよくできていました。")
    elif eye_max[0] >= 1420 or eye_min[0] <= 500:   #左右どちらかを確認した
        eye1 = 5
        print("もう少し左右を確認しましょう。")
    else:                                           #左右どちらも確認していない
        eye1 = 0
        print("もっと左右を確認しましょう。")


    sum = sum + eye1

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
    print("<h4>評価 コメント</h4>")
    if speed_mean <= 20:
        s1 = 8
        print("徐行ができていました。")
    elif speed_mean <= 30:
        s1 = 5
        print("もう少し速度を落としましょう。")
    else:
        s1 = 0
        print("もっと速度を落としましょう。")

    sum = sum + s1

def showStat2(speed_data):
    global s2
    global sum
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
    print("<h4>評価 コメント</h4>")
    if speed_mean <= 20:
        s2 = 8
        print("よくできていました。")
    elif speed_mean <= 30:
        s2 = 5
        print("もう少し速度を落としましょう。")
    else:
        s2 = 0
        print("もっと速度を落としましょう。")

    sum = sum + s2

def showStat3(eye_data, speed_data):
    global eye2
    global s3
    global sum
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
    print("<h4>評価 コメント</h4>")
    if eye_max[0] >= 1420 and eye_min[0] <= 500 :   #左右を確認した
        eye2 = 8
        print("左右確認はできていました。")
    elif eye_max[0] >= 1420 and eye_min[0] <= 500 : #左右どちらかを確認した
        eye2 = 5
        print("もう少し左右を確認しましょう。")
    else:                                           #左右を確認していない
        eye2 = 0
        print("もっと左右を確認しましょう。")

    sum = sum + eye2

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
    print("<h4>評価 コメント</h4>")
    if speed_min == 0:
        s3 = 10
        print("一時停止が出来ていました。")
    else:
        s3 = 0
        print("一時停止が出来ていませんでした。")

    sum = sum + s3

# グラフの描画
def plotGraph1(file_name1, file_name2):
    print("<div>")
    print("<table>")
    print("<tr>")
    print(f"<td><img src='../fig/{file_name1}'></td>")
    print(f"<td><img src='../fig/{file_name2}'></td>")
    print("</tr>")
    print("</table>")

def plotGraph2(file_name1):
    print(f"<img src='../fig/{file_name1}'>")

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
showStat1(eye_data, speed_data)
plotGraph1("eye-1.png", "speed-1.png")

#print(eye_data.to_html())
#print(focus_data.to_html())

# トラック
print("<h2>トラック</h2>")
target_x = 7160
distance = 50
eye_data, speed_data, focus_data = getData(target_x - distance, target_x + distance)
makeSpeedGraph(speed_data, "speed-2.png")
showStat2(speed_data)
plotGraph2("speed-2.png")

# 第２交差点
print("<h2>第2交差点</h2>")
target_x = 7300
distance = 50
eye_data, speed_data, focus_data = getData(target_x - distance, target_x + distance)
makeEyeGraph(eye_data, "eye-3.png")
makeSpeedGraph(speed_data, "speed-3.png")
showStat1(eye_data, speed_data)
plotGraph1("eye-3.png", "speed-3.png")

# 第3交差点
print("<h2>第3交差点(停止1)</h2>")
target_x = 7430
distance = 50
eye_data, speed_data, focus_data = getData(target_x - distance, target_x + distance)
makeEyeGraph(eye_data, "eye-4.png")
makeSpeedGraph(speed_data, "speed-4.png")
showStat3(eye_data, speed_data)
plotGraph1("eye-4.png", "speed-4.png")

# 第4交差点
print("<h2>第4交差点</h2>")
target_x = 7580
distance = 50
eye_data, speed_data, focus_data = getData(target_x - distance, target_x + distance)
makeEyeGraph(eye_data, "eye-5.png")
makeSpeedGraph(speed_data, "speed-5.png")
showStat1(eye_data, speed_data)
plotGraph1("eye-5.png", "speed-5.png")

# 歩行者
print("<h2>歩行者</h2>")
target_x = 7710
distance = 50
eye_data, speed_data, focus_data = getData(target_x - distance, target_x + distance)
makeSpeedGraph(speed_data, "speed-6.png")
showStat2(speed_data)
plotGraph2("speed-6.png")

# 第5交差点
print("<h2>第5交差点(停止2)</h2>")
target_x = 7865
distance = 50
eye_data, speed_data, focus_data = getData(target_x - distance, target_x + distance)
makeEyeGraph(eye_data, "eye-7.png")
makeSpeedGraph(speed_data, "speed-7.png")
showStat3(eye_data, speed_data)
plotGraph1("eye-7.png", "speed-7.png")

print("<h1>総合評価</h1>")
print("<h3>点数</h3>")
print("<h4>")
print(sum)
print("</h4>")
print("<p>(※100点満点)</p>")
print("<h3>評価</h3>")
if sum >= 90:
    print("<h4>あなたの運転評価はA評価です。</h4>")
elif sum >= 70:
    print("<h4>あなたの運転評価はB評価です。</h4>")
else:
    print("<h4>あなたの運転評価はC評価です。</h4>")
#print(eye_data.to_html())
#print(focus_data.to_html())
# 全データの表示
#print(log.to_html())

print("</body>")
print("</html>")
