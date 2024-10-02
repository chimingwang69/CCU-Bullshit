from bs4 import BeautifulSoup
import requests
import threading
import time


email = ''
your_sessionid = ''
# 保險用身分證字號
identity_number = ''
# YYYY-MM-DD
birthday = ''
# meat: 葷食    no_need: 自理    vegetarian: 素食
meal = 'meat'

useragent = 'Mozilla/5.0 (X11; Linux; en-US; rv:127.0) Gecko/20160210 Firefox/127.0'
headers = {'User-Agent': useragent}

# 活動的類別


class Event:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def attend(event_id, stop_event):
    '''
    Func attend: 報名活動
    Param event_id: 活動ID, type: str
    Param stop_event: 事件對象, type: threading.Event
    Raises AssertionError: sessionid過期時觸發
    '''
    data = {'email': email, 'identity_number': identity_number,
            'birthday': birthday, 'meal': meal}
    url = f'https://events.lib.ccu.edu.tw/event/add/{event_id}/'
    while True:
        try:
            # threading.Event()被set後停止
            if stop_event.is_set():
                assert False, f'{event_id} : 結束執行緒'
            res = session.get(url, cookies=cookies)
            soup = BeautifulSoup(res.text, 'html.parser')
            # check用戶欄位的狀態是否需登入
            status = soup.find_all('a', title='登入')
            for info in status:
                if info.text == '登入':
                    assert False, '請更新sessionid'
            # 取得活動報名頁的csrfmiddlewaretoken
            csrfmiddlewaretoken = soup.find(
                'input', {'name': 'csrfmiddlewaretoken'})['value']
            data['csrfmiddlewaretoken'] = csrfmiddlewaretoken
            res = session.post(
                url, data=data, headers=headers, cookies=cookies)
        except AssertionError as msg:
            print(msg)
            break
        except:
            pass
    return None


# 取得列表內所有服務學習活動的id
# var events: 用來儲存活動的物件, type: list
events = []
# 接受報名中的活動
all_event_url = 'https://events.lib.ccu.edu.tw/event/search/?time=join'
# 我的活動頁面
my_event_url = 'https://events.lib.ccu.edu.tw/my/'
cookies = {'sessionid': your_sessionid}
session = requests.session()
res = session.get(all_event_url, cookies=cookies)
soup = BeautifulSoup(res.text, 'html.parser')
# 列出所有活動link
links = soup.find_all(
    'a', href=lambda href: href and href.startswith('/event/detail/list/'))
# 從所有活動中篩選出名字內含服務學習的活動
for link in links:
    if link.get('title').find('服務學習') != -1:
        # var event_id: 活動的ID, type: str
        event_id = link.get('href').split('/')[4]
        # var event_name: 活動的名稱, type: str
        event_name = link.get('title')
        event_id = Event(event_id, event_name)
        events.append(event_id)
        print(f'{event_id.id}:{event_name}')


# 多執行緒
threads = []
# var stop_events: 儲存threading.Event() aka 事件對象(Event Object) 這裡是用來停止執行緒, type: list
stop_events = [threading.Event() for _ in range(len(events))]
for i, event in enumerate(events):
    threads.append(threading.Thread(
        target=attend, args=(event.id, stop_events[i])))
    event.threads = i
    threads[i].start()


# 監控events.lib.ccu.edu.tw/my/的活動 有的話就結束該threads
# var attended_event: 報名成功的活動, type: list
attended_event = []
while events:
    res = session.get(my_event_url, cookies=cookies)
    soup = BeautifulSoup(res.text, 'html.parser')
    # var my_events : https://events.lib.ccu.edu.tw/my/ 內所有已報名活動, type : list
    my_events = soup.find_all('a', class_='color_secondary',
                              href=lambda href: href and href.startswith('/event/detail/MyEventList/'))
    for item in my_events:
        if item.get('href').split('/')[4] not in attended_event:
            attended_event.append(item.get('href').split('/')[4])
    for event in events:
        # 如果該event在已報名活動內 設stop_events[n]的事件對象  把該event從events刪掉
        # 直接continue跳下一個活動
        if event.id in attended_event:
            print(f'成功報名: {event.id} {event.name}')
            stop_events[event.threads].set()
            events.remove(event)
            continue
        # 如果執行緒意外停止 把該event從events刪掉
        if not threads[event.threads].is_alive():
            events.remove(event)
    time.sleep(60)
for t in threads:
    t.join()
print('done!')
