import requests
import re
import time
local = time.strftime("%Y.%m.%d")
url = 'http://cn.bing.com/'
con = requests.get(url)
content = con.text
reg = r"(az/hprichbg/rb/.*?.jpg)"
a = re.findall(reg, content, re.S)[0]
print(a)
picUrl = url + a
read = requests.get(picUrl)
with open(f'{local}.jpg', 'wb') as f:
    f.write(read.content)
