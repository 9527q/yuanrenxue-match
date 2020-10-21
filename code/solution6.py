import requests
import execjs
import time

with open('s6.js') as f:
    js = execjs.compile(f.read())

sum_num = 0
window_o = 1
q = ''
for page_no in range(1, 6):
    timestamp = int(time.time()) * 1000
    m = js.call('z', timestamp, 1)
    q = f'{1}-{timestamp}|'
    r = requests.get(
        'http://match.yuanrenxue.com/api/match/6',
        params={
            'page': page_no,
            'm': m,
            'q': q,
        }
    )
    # print(r.request.url)
    window_o += 1
    for i in r.json()['data']:
        v = i['value']
        sum_num += v * 24
    print(f'第 {page_no} 页解析完成')
    print(sum_num)

print(f'总合 {sum_num}')
