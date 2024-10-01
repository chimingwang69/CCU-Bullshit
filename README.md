# CCU-Bullshit

中正大學服學講座

> [!WARNING]
> 本腳本僅用學習以events.lib.ccu.edu.tw為例發送http請求(post&get)與回應之解讀
> 而發生包括但不限於帳號被鎖、活動被刪、癱瘓系統遭依中華民國刑法§360起訴，本人一概不承擔任何責任

## 1. Description

受夠那些白癡服學了嗎?

什麼還有兩場講座要聽??

幹這些講者怎麼看這都沒啥料

上台只會講一堆Bullshit浪費時間

然後又搶不到要現場候補

## 2. Requirement

| 套件           | 版本 |
| -------------- | ---- |
| Beautiful Soup |      |
| Request        |      |

## 3. Usage

### Step1.

使用單一入口登入智慧化活動暨報名系統 如下圖

![image](https://github.com/chimingwang69/CCU-Bullshit/blob/main/img/1.png)

### Step2.

打開DevTools(以Chrome為例) 找到 `https://events.lib.ccu.edu.tw`的cookie
把sessionid複製起來

![image](https://github.com/chimingwang69/CCU-Bullshit/blob/main/img/2.png)

### Step3.

填好個人資訊

下面是範例

```python
email            =     'FuckyouCCUSL@ccu.edu.tw'
your_sessionid   =     'hahaccuslissuck87idiot7414biatch'
#保險用身分證字號
identity_number  =     'A948730678'
#YYYY-MM-DD
birthday         =     '1937-07-07'
```

## 4. Note

1. 此腳本需要手動更新sessionid
2. 可在報名開始前先打開
3. ~~沒有寫自動停止的機制，請自行去[我的活動](https://events.lib.ccu.edu.tw/my/)檢查是否有搶到並手動關閉~~ v2有了

```
 ~~
```


```
 ~~
```
