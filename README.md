# DriveingFeedbackReport

UC-win/roadのログファイルから，運転結果の振り返りレポートを生成する．

## 使い方

Pythonでウェブサーバを起動する．
このとき，`--log`でログファイルを指定する．

```
$python server.py --log data/imai-log1.csv
```

規定のブラウザでレポートが表示される．
