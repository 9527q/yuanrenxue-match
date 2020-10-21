import requests
import base64
import re
from fontTools.ttLib import TTFont
import time

# TTFont打开字体文件

# 将字体文件保存为可读的xml文件

# 找字体的映射关系，字体的映射关系在cmap中体现


FILENAME_TTF = './s7.ttf'
FILENAME_XML = './s7-font.xml'
RE_GLYPH = re.compile(r'<TTGlyph.*?</TTGlyph>')
RE_CONTOUR = re.compile(r'<contour>.*?</contour>')
RE_PT = re.compile(r'<pt.*?/>')
USERNAMES = ['极镀ギ紬荕', '爷灬霸气傀儡', '梦战苍穹', '傲世哥', 'мaη肆風聲', '一刀メ隔世', '横刀メ绝杀', 'Q不死你R死你', '魔帝殤邪', '封刀不再战', '倾城孤狼', '戎马江湖', '狂得像风', '影之哀伤', '謸氕づ独尊', '傲视狂杀', '追风之梦', '枭雄在世', '傲视之巅', '黑夜刺客', '占你心为王', '爷来取你狗命', '御风踏血', '凫矢暮城', '孤影メ残刀', '野区霸王', '噬血啸月', '风逝无迹', '帅的睡不着', '血色杀戮者', '冷视天下', '帅出新高度', '風狆瑬蒗', '灵魂禁锢', 'ヤ地狱篮枫ゞ', '溅血メ破天', '剑尊メ杀戮', '塞外う飛龍', '哥‘K纯帅', '逆風祈雨', '恣意踏江山', '望断、天涯路', '地獄惡灵', '疯狂メ孽杀', '寂月灭影', '骚年霸称帝王', '狂杀メ无赦', '死灵的哀伤', '撩妹界扛把子', '霸刀☆藐视天下', '潇洒又能打', '狂卩龙灬巅丷峰', '羁旅天涯.', '南宫沐风', '风恋绝尘', '剑下孤魂', '一蓑烟雨', '领域★倾战', '威龙丶断魂神狙', '辉煌战绩', '屎来运赚', '伱、Bu够档次', '九音引魂箫', '骨子里的傲气', '霸海断长空', '没枪也很狂', '死魂★之灵']
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="cache-control" content="no-cache">
    <title></title>
    <style type="text/css">
        @font-face {
            font-family: "pixelEn";
            src: url("ttf_filename");
        }
        p {
            font-family: "pixelEn";
            font-size: 24px;
        }
    </style>
</head>
<body>
    pppp
</body>
</html>
"""

CNTPT2INT = {
    (10,): 1,
    (29, 12): 9,
    (44,): 3,
    (13, 13): 0,
    (10,): 1,
    (30,): 2,
    (11, 4): 4,
    (7,): 7,
    (37,): 5,
    (32, 13, 12): 8,
    (28, 13): 6,
}


def parse_ttf_xmlfile():
    res = {}
    with open(FILENAME_XML) as f:
        xml = f.read().replace('\n', '').replace('\r', '')
    is_first = True
    for glyph_str in RE_GLYPH.findall(xml):
        if is_first:
            is_first = False
            continue
        name = glyph_str[15:22].replace('uni', '&#x')
        contours = RE_CONTOUR.findall(glyph_str)
        cnt_contour = len(contours)
        cnt_pts = tuple()
        for contour_str in contours:
            cnt_pt = len(RE_PT.findall(contour_str))
            cnt_pts += (cnt_pt,)
        # print(name, cnt_contour, cnt_pts)
        res[name] = CNTPT2INT[cnt_pts]

    return res


def parse_ttf_data(ttf_data_str):
    # name_str -> int
    with open(FILENAME_TTF, 'wb') as f:
        f.write(base64.b64decode(ttf_data_str))
    font = TTFont(FILENAME_TTF)
    font.saveXML(FILENAME_XML)
    time.sleep(1)
    return parse_ttf_xmlfile()


max_number = 0
max_name = ''
for page_no in range(1, 6):
    r = requests.get(f'http://match.yuanrenxue.com/api/match/7?page={page_no}')
    data = r.json()
    woff1 = data['woff']
    data = data['data']
    name2int = parse_ttf_data(woff1)
    i_delta = 1
    for line in data:
        number_str = ''
        for i in line['value'].strip().split(' '):
            number_str += str(name2int[i])
        number = int(number_str)
        username = USERNAMES[(page_no-1)*10 + i_delta]
        i_delta += 1
        if number > max_number:
            max_number = number
            max_name = username
        # print(username, number)
    # ss = []
    # for i in data:
    #     ss.append(f'<p>{i["value"]}<p>')
    # with open('s7.html', 'w') as f:
    #     f.write(HTML.replace('ttf_filename', FILENAME_TTF)
    #             .replace('pppp', '\n'.join(ss)))
    print(f'第 {page_no} 页解析成功')


print(max_name, max_number)

