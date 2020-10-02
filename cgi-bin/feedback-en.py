#!/usr/bin/env python

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sys
import cgi
import io

# スクリーンサイズ
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# スコア
score_eye = 0
score_speed = 0

# 閾値    
threshold_eye = 500
threshold_speed = 20

# 文字化けの解消
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding = 'utf-8')

# GETリクエストの取得
fields = cgi.FieldStorage()
log_file = fields.getvalue("log")

# CSVファイルの読込
log = pd.read_csv(log_file, sep=",")

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
    eye_data.plot.scatter(x="focus_x", y="focus_y", xlim=[0, SCREEN_WIDTH], ylim=[0, SCREEN_HEIGHT], label="eye point")

    center = eye_data.mean()
    plt.scatter(x=center[0], y=center[1], color="red", label="average", s=40)
    plt.legend()
    
    plt.xlabel("X[px]")
    plt.ylabel("Y[px]")
    plt.title("Eye Moving")
    plt.savefig("fig/" + file_name)
    plt.close("all")

# 速度データのグラフ化
def makeSpeedGraph(speed_data, file_name):
    plt.figure()
    speed_data.plot(x="x", y="speed")

    start_x = speed_data.iloc[1]["x"]
    goal_x = speed_data.iloc[-1]["x"]
    x = np.arange(start_x-10, goal_x+10, 1)
    y = np.full(x.size, speed_data.mean()[1])
    plt.plot(x, y, label="average")
    plt.legend()
    
    plt.xlabel("Distance[km]")
    plt.ylabel("Speed[km/h]")
    plt.title("Speed")
    plt.savefig("fig/" + file_name)
    plt.close("all")

# 視線の評価
def showEyeStat(eye_data):
    
    # 統計量の取得
    eye_mean = eye_data.mean()
    eye_std = eye_data.std()
    eye_max = eye_data.max()
    eye_min = eye_data.min()

    # 統計量の表示
    print("<div>")
    print("<h3>Your Eye-Moving</h3>")
    print("<table border='1' style='border-collapse: collapse'>")
    print(f"<tr><th>Average<th> <td>X:{round(eye_mean[0], 2)}[px] Y:{round(eye_mean[1], 2)}[px]</td></tr>")
    print(f"<tr><th>Standard Deviation<th> <td>X:{round(eye_std[0], 2)}[px] Y:{round(eye_std[1], 2)}[px]</td></tr>")
    print(f"<tr><th>Maximum<th> <td>X:{round(eye_max[0], 2)}[px] Y:{round(eye_max[1], 2)}[px]</td></tr>")
    print(f"<tr><th>Minimum<th> <td>X:{round(eye_min[0], 2)}[px] Y:{round(eye_min[1], 2)}[px]</td></tr>")
    print("</table>")

    # 視線移動のスコア
    score = 0
    
    # 評価コメント
    print("<h4>評価コメント</h4>")
    if eye_max[0] >= SCREEN_WIDTH - threshold_eye and eye_min[0] <= threshold_eye:
        #左右両方を確認
        score = 8
        print("<p>You correctly looked both sides.</p>")
    elif eye_max[0] >= SCREEN_WIDTH - threshold_eye:
        #右だけ確認
        score = 5
        print("<p>You looked the right side only.</p>")
    elif eye_min[0] <= threshold_eye:
        #左だけ確認
        score = 5
        print("<p>You looked the left side only.</p>")        
    else:
        #左右確認なし        
        score = 0
        print("<p>You never looked any side.</p>")

    print("</div>")
        
    return score

# 速度の評価
def showSpeedStat(speed_data):

    # 速度統計量
    speed_mean = speed_data.mean()[1]
    speed_std = speed_data.std()[1]
    speed_max = speed_data.max()[1]
    speed_min = speed_data.min()[1]

    # 統計量の表示
    print("<div>")
    print("<h3>Your Speed</h3>")
    print("<table border='1' style='border-collapse: collapse'>")
    print(f"<tr><th>Average<th> <td>{round(speed_mean, 2)}[km/h]</td></tr>")
    print(f"<tr><th>Standard Deviation<th> <td>{round(speed_std, 2)}[km/h]</td></tr>")
    print(f"<tr><th>Maximum<th> <td>{round(speed_max, 2)}[km/h]</td></tr>")
    print(f"<tr><th>Minimum<th> <td>{round(speed_min, 2)}[km/h]</td></tr>")
    print("</table>")
    
    # 速度のスコア
    score = 0

    # 評価コメント
    print("<h4>評価コメント</h4>")
    if speed_mean <= threshold_speed:
        score = 8
        print("<p>You correctly reduced the speed.</p>")
    elif speed_mean <= (threshold_speed + 10):
        score = 5
        print("<p>You should have reduced the speed slightly. </p>")
    else:
        score = 0
        print("<p>Your speed is over the limit.</p>")

    print("</div>")        

    return score

# 一時停止の評価
def showStopStat(speed_data):

    # 速度統計量
    speed_mean = speed_data.mean()[1]
    speed_std = speed_data.std()[1]
    speed_max = speed_data.max()[1]
    speed_min = speed_data.min()[1]

    print("<div>")    
    print("<h3>Your Speed</h3>")
    print("<table border='1' style='border-collapse: collapse'>")
    print(f"<tr><th>Average<th> <td>{round(speed_mean, 2)}[km/h]</td></tr>")
    print(f"<tr><th>Standard Deviation<th> <td>{round(speed_std, 2)}[km/h]</td></tr>")
    print(f"<tr><th>Maximum<th> <td>{round(speed_max, 2)}[km/h]</td></tr>")
    print(f"<tr><th>Minimum<th> <td>{round(speed_min, 2)}[km/h]</td></tr>")
    print("</table>")
    
    # 一時停止のスコア
    score = 0
    
    print("<h4>評価コメント</h4>")
    if speed_min == 0:
        score = 10
        print("<p>You correctly paused at the intersection.</p>")
    else:
        score = 0
        print("<p>You did not pause at the intersection.</p>")

    print("</div>")

    return score
        

# グラフの描画
def plotGraph(file_names):
    print("<div>")
    print("<table>")
    print("<tr>")
    for file_name in file_names:
        print(f"<td><img src='../fig/{file_name}'></td>")
    print("</tr>")
    print("</table>")
    print("</div>")

print ("Content-type:text/html\n\n")
print("<!DOCTYPE html>")
print("<html>")

print("<head>")
print("<meta charset='utf-8'>")
print("<title>Your Driving Feedback Report</title>")
print("</head>")

print("<body>")
print("<h1>Your Driving Feedback Report</h1>");
print(f"<h2>Log File: {log_file}</h2>")

print("<ul>")
print("<li><a href='#check1'>1st Intersection</a></li>");
print("<li><a href='#check2'>Obstacle: Truck</a></li>");
print("<li><a href='#check3'>2nd Intersection</a></li>");
print("<li><a href='#check4'>3rd Intersection with Stop Sign</a></li>");
print("<li><a href='#check5'>4th Intersection</a></li>");
print("<li><a href='#check6'>Obstacle: Pedestrian</a></li>");
print("<li><a href='#check7'>5th Intersection with Stop Sign</a></li>");
print("<li><a href='#check8'>Your Evaluation</a></li>");
print("</ul>")

# 第１交差点
target_x = 6964
distance = 50
print("<hr>")
print(f"<h2 id='check1'>1st Intersection</h2>")
print(f"<h3>Between from X={target_x-50}[m] to X={target_x+50}[m]</h3>")
print(f"<p><img width='500px' src='../fig/checkpoints/check1.png'></p>")
file_name1 = "eye-1.png"
file_name2 = "speed-1.png"
eye_data, speed_data, focus_data = getData(target_x - distance, target_x + distance)
makeEyeGraph(eye_data, file_name1)
makeSpeedGraph(speed_data, file_name2)
score_eye += showEyeStat(eye_data)
score_speed += showSpeedStat(speed_data)
plotGraph([file_name1, file_name2])

# トラック
target_x = 7160
distance = 50
print("<hr>")
print("<h2 id='check2'>Obstacle: Truck</h2>")
print(f"<h3>Between from X={target_x-50}[m] to X={target_x+50}[m]</h3>")
print(f"<p><img width='500px' src='../fig/checkpoints/check2.png'></p>")
file_name1 = "eye-2.png"
file_name2 = "speed-2.png"
eye_data, speed_data, focus_data = getData(target_x - distance, target_x + distance)
makeSpeedGraph(speed_data, file_name2)
score_speed += showSpeedStat(speed_data)
plotGraph([file_name2])


# 第２交差点
target_x = 7300
distance = 50
print("<hr>")
print(f"<h2 id='check3'>2nd Intersection</h2>")
print(f"<h3>Between from X={target_x-50}[m] to X={target_x+50}[m]</h3>")
print(f"<p><img width='500px' src='../fig/checkpoints/check3.png'></p>")
file_name1 = "eye-3.png"
file_name2 = "speed-3.png"
eye_data, speed_data, focus_data = getData(target_x - distance, target_x + distance)
makeEyeGraph(eye_data, file_name1)
makeSpeedGraph(speed_data, file_name2)
score_eye += showEyeStat(eye_data)
score_speed += showSpeedStat(speed_data)
plotGraph([file_name1, file_name2])

# 第３交差点
target_x = 7430
distance = 50
print("<hr>")
print(f"<h2 id='check4'>3rd Intersection with Stop Sign</h2>")
print(f"<h3>Between from X={target_x-50}[m] to X={target_x+50}[m]</h3>")
print(f"<p><img width='500px' src='../fig/checkpoints/check4.png'></p>")
file_name1 = "eye-4.png"
file_name2 = "speed-4.png"
eye_data, speed_data, focus_data = getData(target_x - distance, target_x + distance)
makeEyeGraph(eye_data, file_name1)
makeSpeedGraph(speed_data, file_name2)
score_eye += showEyeStat(eye_data)
score_speed += showStopStat(speed_data)
plotGraph([file_name1, file_name2])

# 第４交差点
target_x = 7580
distance = 50
print("<hr>")
print(f"<h2 id='check5'>4th Intersection</h2>")
print(f"<h3>Between from X={target_x-50}[m] to X={target_x+50}[m]</h3>")
print(f"<p><img width='500px' src='../fig/checkpoints/check5.png'></p>")
file_name1 = "eye-5.png"
file_name2 = "speed-5.png"
eye_data, speed_data, focus_data = getData(target_x - distance, target_x + distance)
makeEyeGraph(eye_data, file_name1)
makeSpeedGraph(speed_data, file_name2)
score_eye += showEyeStat(eye_data)
score_speed += showSpeedStat(speed_data)
plotGraph([file_name1, file_name2])


# 歩行者
target_x = 7710
distance = 50
print("<hr>")
print("<h2 id='check6'>Obstacle: Pedestrian</h2>")
print(f"<h3>Between from X={target_x-50}[m] to X={target_x+50}[m]</h3>")
print(f"<p><img width='500px' src='../fig/checkpoints/check6.png'></p>")
file_name1 = "eye-6.png"
file_name2 = "speed-6.png"
eye_data, speed_data, focus_data = getData(target_x - distance, target_x + distance)
makeSpeedGraph(speed_data, file_name2)
score_speed += showSpeedStat(speed_data)
plotGraph([file_name2])


# 第５交差点
target_x = 7865
distance = 50
print("<hr>")
print(f"<h2 id='check7'>5th Intersection with Stop Sign</h2>")
print(f"<h3>Between from X={target_x-50}[m] to X={target_x+50}[m]</h3>")
print(f"<p><img width='500px' src='../fig/checkpoints/check7.png'></p>")
file_name1 = "eye-4.png"
file_name2 = "speed-4.png"
eye_data, speed_data, focus_data = getData(target_x - distance, target_x + distance)
makeEyeGraph(eye_data, file_name1)
makeSpeedGraph(speed_data, file_name2)
score_eye += showEyeStat(eye_data)
score_speed += showStopStat(speed_data)
plotGraph([file_name1, file_name2])

# 運転評価
total_score = score_eye + score_speed
print("<hr>")
print("<h2 id='check8'>Your Evaluation</h2>")
print(f"<h3>Eye-Moving Score: {score_eye} / 40 </h3>")
print(f"<h3>Speed Score: {score_speed} / 60 </h3>")
print(f"<h3>Total Score: {total_score} / 100</h3>")

if total_score >= 90:
    print("<h2>Your Driving Evaluation is <em>Rank A</em></h2>")
elif total_score >= 70:
    print("<h2>Your Driving Evaluation is <em>Rank B</em></h2>")
else:
    print("<h2>Your Driving Evaluation is <em>Rank C</em></h2>")


print("</body>")
print("</html>")

