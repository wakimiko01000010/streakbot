# coding: utf-8
import datetime
import time
import os
import requests

user_name = "matsugen1234"
user_url = f"https://kenkoooo.com/atcoder/atcoder-api/results?user={user_name}"

print(user_url)

res = requests.get(user_url).json()

# 今の時間
now = datetime.datetime.fromtimestamp(time.time(), datetime.timezone(datetime.timedelta(hours=9)))


accepted = set()
today_accepted = []
streak_len = 0
out_count = 0
while True: 
    for submit in res:
        submittime = datetime.datetime.fromtimestamp(submit['epoch_second'], datetime.timezone(datetime.timedelta(hours=9)))

        problemid = submit['problem_id']

        # ステータスがAC以外なら無視
        if submit['result'] != 'AC':
            continue

        # 過去に解いた問題なら解答済みセットに追加
        if submittime.date() < now.date():
            accepted.add(problemid)
        
        # 今日解いた && 今までに解いたこと無いなら新規リストに追加
        if submittime.date() == now.date() and problemid not in accepted:
            today_accepted.append(submit)

    # リストに要素がある（初めて解いた問題がある)ならストリーク+1
    if len(today_accepted) != 0:
        streak_len += 1
        now = now - datetime.timedelta(days=1)
        today_accepted = []
        accepted = set()
    else :
        out_count += 1
        now = now - datetime.timedelta(days=1)
        today_accepted = []
        accepted = set()

    # 今日まだ解いていない場合があるので、2回空いたらアウトにする。
    # ここいらないかも
    if out_count > 1:
        break

print('streak is ', end="")
print(streak_len)
