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
# meat:葷食 no_need:自理 vegetarian:素食
meal = 'meat'

useragent = 'Mozilla/5.0 (X11; Linux; en-US; rv:127.0) Gecko/20160210 Firefox/127.0'
headers = {'User-Agent': useragent}


class Event:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def attend(event_id, stop_event):
    data = {'email': email, 'identity_number': identity_number,
            'birthday': birthday, 'meal': meal}
    url = f'https://events.lib.ccu.edu.tw/event/add/{event_id}/'
    while True:
        try:
            if stop_event.is_set():
                assert False, f'{event_id} : 結束執行緒'
            res = session.get(url, cookies=cookies)
            soup = BeautifulSoup(res.text, 'html.parser')
            status = soup.find_all('a', title='登入')
            for info in status:
                if info.text == '登入':
                    assert False, '請更新sessionid'
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
    return 0


# 取得列表內所有服務學習活動的id
events = []
all_event_url = 'https://events.lib.ccu.edu.tw/event/search/?time=join'
my_event_url = 'https://events.lib.ccu.edu.tw/my/'
cookies = {'sessionid': your_sessionid}
session = requests.session()
res = session.get(all_event_url, cookies=cookies)
soup = BeautifulSoup(res.text, 'html.parser')
# 列出所有活動link
links = soup.find_all(
    'a', href=lambda href: href and href.startswith('/event/detail/list/'))
for link in links:
    if link.get('title').find('服務學習') != -1:
        event_name = link.get('title')
        event_id = link.get('href').split('/')[4]
        event_id = Event(event_id, event_name)
        events.append(event_id)
        print(f'{event_id.id}:{event_name}')


# 多執行緒
threads = []
stop_events = [threading.Event() for _ in range(len(events))]
for i, event in enumerate(events):
    threads.append(threading.Thread(
        target=attend, args=(event.id, stop_events[i])))
    event.threads = i
    threads[i].start()


# 監控events.lib.ccu.edu.tw/my/的活動 有的話就結束該threads
attended_event = []
while True:
    time.sleep(60)
    res = session.get(my_event_url, cookies=cookies)
    soup = BeautifulSoup(res.text, 'html.parser')
    my_events = soup.find_all('a', class_='color_secondary',
                              href=lambda href: href and href.startswith('/event/detail/MyEventList/'))
    for item in my_events:
        if item.get('href').split('/')[4] not in attended_event:
            attended_event.append(item.get('href').split('/')[4])
    for event in events:
        if event.id in attended_event:
            print(f'成功報名: {event.id} {event.name}')
            stop_events[event.threads].set()
            events.remove(event)
    if not events:
        break
for t in threads:
    t.join()
print('done!')
