# coding: utf-8
import datetime
import time
import os
import requests
from slackbot.bot import respond_to
import requests

# ストリークが知りたいユーザのID
user_name = ["matsugen1234", "I4n", "wakimiko"]

@respond_to('streak')
def show_streak(message):
    for x in range(len(user_name)):
        user_url = f"https://kenkoooo.com/atcoder/atcoder-api/results?user={user_name[x]}"

        print(user_url)

        res = requests.get(user_url).json()

        # 今の時間
        now = datetime.datetime.fromtimestamp(time.time(), datetime.timezone(datetime.timedelta(hours=9)))

        today = now


        accepted = set()
        day_accepted = []
        streak_len = 0

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
                    day_accepted.append(submit)

            # リストに要素がある（初めて解いた問題がある)ならストリーク+1
            if len(day_accepted) != 0:
                streak_len += 1
            elif now.date() == today.date():
                pass
            else :
                break

            now = now - datetime.timedelta(days=1)
            day_accepted = []
            accepted = set()

        message.send(user_name[x] + "さんのstreak数は現在 " + str(streak_len) + "です")
