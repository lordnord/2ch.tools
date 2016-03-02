# coding: utf8
# image must be 920 x 780

import time
import sys
import StringIO

import requests
import Image

import funcs

coords = (
   ((0, 0, 200, 200),
    (240, 0, 440, 200),
    (480, 0, 680, 200),
    (720, 0, 920, 200)),
   ((0, 290, 200, 490),
    (240, 290, 440, 490),
    (480, 290, 680, 490),
    (720, 290, 920, 490)),
   ((0, 580, 200, 780),
    (240, 580, 440, 780),
    (480, 580, 680, 780),
    (720, 580, 920, 780))
)

_, threadlink, imgpath = sys.argv
im = Image.open(imgpath)
data = funcs.basic_data(threadlink)

for i in range(3):
    files = {}
    for x in range(4):
        buffer = StringIO.StringIO()
        im.crop(coords[i][x]).save(buffer, "jpeg")
        files['image{}'.format(x + 1)] = buffer.getvalue()
    response = requests.post('https://2ch.hk/makaba/posting.fcgi', data=data,  files=files)
    print(response.status_code)
    time.sleep(20)

