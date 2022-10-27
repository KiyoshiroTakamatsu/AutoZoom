#以下の*.pngはサイト内の写真の一部。
#pyautoguiの認識能力で、timeによる固定時間待つのではなく、認識したらクリックする仕組み。
import datetime as d
import pyautogui as py
import webbrowser as w
import time as t
import sys
import os

os.chdir(os.path.dirname(__file__))

#nameで指定した写真(dendai_page_access内)を検知したらクリックするメソッド
def clickPic(name, week, time, dt1):
    while True:
        posi = py.locateCenterOnScreen(name, confidence = 0.9)
        if posi != None:
            print(week + '\n' + str(time) + '限')
            py.click(posi.x, posi.y-270)
            break
        else:
            print('unmatch')
        error_check_timeout(dt1, 4)

#授業時間外であるがためのエラー
def error_1():
    print('error:授業時間外です')

#タイムアウトによるエラー
def error_check_timeout(dt1, error_code):
    dt2 = t.time()
    deltime = int(dt2-dt1)
    if(deltime>19):
        sys.exit('error:タイムアウトしました(経過時間' + str(deltime) + '秒)\nerror_code:' + str(error_code))
    else:
        pass
    

#スタート画面からwebclassまで遷移

w.open('学校のWebClassのURL')


#(以下pageのUIによっては反応しないため注意)

#Window最大化
dt1 = t.time()
while True:
    posi1 = py.locateCenterOnScreen('zoomscreen.png', confidence = 0.9)
    posi2 = py.locateCenterOnScreen('noneedzoom.png', confidence = 0.9)
    if posi1 != None:
        py.click(posi1)
        print('拡大しました')
        break
    elif posi2 != None:
        print('拡大の必要なし')
        break
    error_check_timeout(dt1, 1)

#webclassログイン画面ならログインボタンを押す
dt1 = t.time()
while py.locateOnScreen('webclass.png', confidence = 0.8) == None:
    print('ログインボタンを探しています')
    pos = py.locateCenterOnScreen('webclass_login.png', confidence = 0.8)
    if(pos != None):
        py.click(pos)
        print('ログインしました')
        break
    error_check_timeout(dt1, 2)

#webclassについたら画面をスクロール
dt1 = t.time()
while True:
    print('スクロール待機中')
    if py.locateOnScreen('webclass.png', confidence = 0.8) != None:
        py.moveTo(1220, 475)
        py.scroll(-500)
        print('スクロールしました')
        break
    error_check_timeout(dt1, 3)

#dtの現在時刻と曜日を取得してそれに合ったページを開く
dt = d.datetime.today()
now = str(dt.time())#現在時刻を取得しstr型にキャスト
week = dt.strftime('%A')#曜日を英語で取得

#以下取得した時間と曜日から適切な教材URL、zoomにアクセス。
# 対面がほとんどであった都合上、水曜3限のみzoomアクセス。

if now >= '09:00:00'and now <= '11:00:00':#1限
    if week == 'Monday':
        clickPic('Mon_1.png', week, 1, t.time())
    elif week == 'Tuesday':
        clickPic('Tues_1.png', week, 1, t.time())
    elif week == 'Thursday':
        clickPic('Thu_1.png', week, 1, t.time())
    else:
        error_1()
elif now > '11:00:00' and now <= '12:50:00':#２限
    if week == 'Monday':
        clickPic('Mon_2.png', week, 2, t.time())
    elif week == 'Wednesday':
        clickPic('Wed_2.png', week, 2, t.time())
    elif week == 'Thursday':
        clickPic('Thu_2.png', week, 2, t.time())
    elif week == 'Friday':
        clickPic('Tues_3.png', week, 2, t.time())#金曜2限=火曜3限
    else:
        error_1()
elif now > '12:50:00' and now <= '15:20:00':#3限
    if week == 'Monday':
        clickPic('Mon_3.png', week, 3, t.time())
    elif week == 'Tuesday':
        clickPic('Tues_3.png', week, 3, t.time())
    elif week == 'Wednesday':
        clickPic('Wed_3.png', week, 3, t.time())
        w.open('zoomURL')
        while py.locateOnScreen('webclass.png', confidence = 0.8) == None:
            print('zoomアクセスボタンを探しています')
            pos = py.locateCenterOnScreen('zoom_page.png', confidence = 0.8)
            if(pos != None):
                py.click(pos)
                print('zoomに入りました')
                break
        error_check_timeout(dt1, 2)
            
    elif week == 'Thursday':
        clickPic('Thu_3.png', week, 3, t.time())
    else:
        error_1()
elif now > '15:20:00' and now <= '17:10:00':#４限
    if week == 'Monday':
        clickPic('Mon_4.png', week, 4, t.time())
    elif week == 'Thursday':
        clickPic('Thu_4.png', week, 4, t.time())
    else:
        error_1()
else:
    error_1()