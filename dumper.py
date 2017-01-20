# coding: utf8

import os
import sys
import time
import random
import requests

import funcs

NUMBER = 4
PAUSE = 20

session = requests.Session()
_, thread, folder = sys.argv
del _
all = funcs.accepted_files(folder)

while len(all) >= NUMBER:
    images = {}
    for i in range(NUMBER):
        filename = random.choice(all)
        all.remove(filename)
        path = os.path.join(folder, filename)
        images['image{}'.format(i + 1)] = open(path, 'rb').read()
    response = session.post(
        'https://2ch.hk/makaba/posting.fcgi', 
        data = funcs.basic_data(thread),  
        files = images,
        )
    print (response.status_code)
    time.sleep(PAUSE)
