import requests
from collections import Counter

# Host: match.yuanrenxue.com


h1 = """
Connection: keep-alive
Content-Length: 0
Accept: */*
Origin: http://match.yuanrenxue.com
Referer: http://match.yuanrenxue.com/match/3
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
"""
h = """
Connection: keep-alive
Content-Length: 0
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36
Accept: */*
Origin: http://match.yuanrenxue.com
Referer: http://match.yuanrenxue.com/match/3
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
"""


ss = requests.Session()

h1 = dict(line.split(': ') for line in h.strip().split('\n'))
h = dict(line.split(': ') for line in h.strip().split('\n'))
values = []
for i in range(1, 6):
    r = ss.post('http://match.yuanrenxue.com/logo', headers=h1)
    print(r.headers)
    r = ss.get(f'http://match.yuanrenxue.com/api/match/3?page={i}', headers=h)
    for data in r.json()['data']:
        values.append(data['value'])
    print(f'第 {i} 页爬取成功')

print('众数 数量')
print(*sorted(Counter(values).items(), key=lambda i: i[1])[-1])
