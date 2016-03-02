# coding: utf8

import time
import os
import sys
import json
import re
import random

import requests
requests = requests.Session()

import funcs

# todo
# исправить вложенные спойлеры


def parse(post):
    all = {
    '<br>': '\n',
    '<em>': '[i]',
    '</em>': '[/i]',
    '<strong>': '[b]',
    '</strong>': '[/b]',
    '<sup>': '[sup]',
    '</sup>': '[/sup]',
    '</sub>': '[/sub]',
    '<sub>': '[sub]',
    '<span class="spoiler">(?P<x>.*)</span>': '[spoiler]\g<x>[/spoiler]',
    '<span class="unkfunc">(?P<x>.*)</span>': '\g<x>', # >quoting
    '<span class="u">(?P<x>.*)</span>': '[u]\g<x>[/u]', # under line
    '<span class="o">(?P<x>.*)</span>': '[o]\g<x>[/o]', # upper line
    '<span class="s">(?P<x>.*)</span>': '[s]\g<x>[/s]', # middle line
    '<a href=".*" class="post-reply-link" data-thread="\d*" data-num="(?P<x>\d*)">>>\d*</a>': '>>\g<x>', 
    '<a href="(?P<x>.*)" target="_blank">.*</a>': '\g<x>', # web link
    '<a href="mailto:.*">(?P<x>.*)</a>': 'mailto:\g<x>',
    }

    for key, value in all.items():
        post = re.sub(key, value, post)
    return post


class App:
    def __init__(self):
        with open('settings.json') as f:
            setup = json.load(f)
        self.data = funcs.basic_data(setup['thread'])
        self.apilink = setup['thread'].replace('.html', '.json')
        
        self.avatar = setup['avatar']
        proxy = setup['proxy']
        if proxy:
            requests.proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy,
                }

        if setup['sage']:
            self.data['email'] = 'sage'
        
        self.run()
        
    def build_data(self):
        # посты для репоста из того же треда
        page = requests.get(self.apilink)
        #print(page.text)
        page = page.json()
        all = page['threads'][0]['posts']
        msg = parse(random.choice(all)['comment'])
        
        
        last = all[-1]['hidden_num']
        if '>>' in msg:
            # заменяем ссылки в посе на последний пост в треде
            msg = re.sub('>>\d+', '>>' + last, msg)
        else:
            # если ссылок нет - вставляем ссылку на последний пост в треде
            msg = '>>' + last + '\n' + msg
        
        data = {'comment': msg}
        data.update(self.data)
        return data

    def run(self):
        files = {}
        if self.avatar:
            filename = random.choice(funcs.accepted_files('pics'))
            filepath = os.path.join('pics', filename)
            files['image1'] = open(filepath, 'rb').read()
        response = requests.post(
            'https://2ch.hk/makaba/posting.fcgi', 
            data=self.build_data(),  
            files=files
        )
        print(response.status_code)
        time.sleep(20)
        self.run()
    

App()