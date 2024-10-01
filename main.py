import requests
from bs4 import BeautifulSoup

email            =     ''
your_sessionid   =     ''
#保險用身分證字號
identity_number  =     ''
#YYYY-MM-DD
birthday         =     ''


data = {'email':email,'identity_number':identity_number,'birthday':birthday}
useragent = 'Mozilla/5.0 (X11; Linux; en-US; rv:127.0) Gecko/20160210 Firefox/127.0'
headers = {'User-Agent': useragent}

# 取得列表內所有服務學習活動的id
event_url = 'https://events.lib.ccu.edu.tw/event/search/?time=join'
events=[]
cookies={'sessionid':your_sessionid}
session= requests.session()
res=session.get(event_url,cookies=cookies)
soup = BeautifulSoup(res.text, 'html.parser')



# 活動link含有class="remove_underline bg_hover_blackOpacity05 w-100"
links = soup.find_all('a', class_="remove_underline bg_hover_blackOpacity05 w-100")
for link in links:
    if link.get('title').find('服務學習') != -1:
        event_name=link.get('title')
        event_id=link.get('href').split('/')[4]
        events.append(event_id)
        print(f'{event_id}:{event_name}')


while True:
    try:
        for event in events:
            url=f'https://events.lib.ccu.edu.tw/event/add/{event}/'
            res=session.get(url,cookies=cookies)
            soup = BeautifulSoup(res.text, 'html.parser')
            status=soup.find_all('a', title='登入')
            for info in status:
                if info.text=='登入':
                    assert False, '請更新sessionid'
            csrfmiddlewaretoken = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
            data['csrfmiddlewaretoken'] = csrfmiddlewaretoken
            res = session.post(url, data=data, headers=headers,cookies=cookies)
    except AssertionError as msg:
        print(msg)
        break
    except:
        continue




