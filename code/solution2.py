import requests
import execjs

with open('s2.js', 'r', encoding='utf8') as f:
    js = execjs.compile(f.read())
    m = js.call('get_m')

h = """
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Referer: http://match.yuanrenxue.com/match/2
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36
X-Requested-With: XMLHttpRequest
"""
h = dict(line.split(': ') for line in h.strip().split('\n'))

value_sum = 0
for page_no in range(1, 6):
    r = requests.get(
        f'http://match.yuanrenxue.com/api/match/2?page={page_no}',
        headers=h, cookies={'m': m}
    )
    data = r.json()
    for i in data['data']:
        value_sum += i['value']
    print(f'第 {page_no} 页解析完成')

print(f'发布日总和 {value_sum}')
