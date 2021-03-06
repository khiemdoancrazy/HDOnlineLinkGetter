#!/usr/bin/python3

import requests
import re
import json


def verify_link(link):
    result = re.match(r'https?:\/\/hdonline.vn\/[\w-]+.html', link, re.M | re.I)
    if result is None:
        return False
    return True


def get_link_video(link):
    headers = dict()
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch'
    headers['Accept-Language'] = 'en-US,en;q=0.8,vi;q=0.6'
    headers['Connection'] = 'keep-alive'
    headers['Host'] = 'hdonline.vn'
    headers['Upgrade-Insecure-Requests'] = '1'
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'

    r = requests.get(link, headers=headers)
    r.close()

    # print(r.text)
    # print(r.headers)

    # lay cooie
    cookie = re.search(r'__cfduid=[\w]+', r.headers['Set-Cookie'], re.M | re.I).group()

    # lay PHPSESSID
    php_sess_id = re.search(r'PHPSESSID=[\w]+', r.headers['Set-Cookie'], re.M | re.I).group()

    # lay fid
    fid = re.search(r'PlayFilm.*\d+', r.text, re.M | re.I).group()
    fid = re.search(r'\d+', fid, re.M | re.I).group()

    # lay token
    token = re.search(r'\w{86,96}.*\d{10}', r.text, re.M | re.I).group()
    token = token.replace('|', '-')

    headers = dict()
    headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch'
    headers['Accept-Language'] = 'en-US,en;q=0.8,vi;q=0.6'
    headers['Cache-Control'] = 'max-age=0'
    headers['Connection'] = 'keep-alive'
    headers['Cookie'] = cookie +'; ' + php_sess_id + ';'
    headers['Host'] = 'hdonline.vn'
    headers['Referer'] = link
    headers[
        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'

    xmlplay_url = 'http://hdonline.vn/frontend/episode/xmlplay?ep=1&fid=' + fid + '&token=' + token + '&format=json'
    r = requests.get(xmlplay_url, headers=headers)
    r.close()

    data = json.loads(r.text)
    for i in data['level']:
        print(i['label'] + ': ' + i['file'])

    for i in data['subtitle']:
        print('subtitle: ' + i['file'])


if __name__ == "__main__":
    link = input('Enter url: ')
    if verify_link(link) is False:
        print('Duong dan khong hop le!')
        exit()
    link = link.strip()
    get_link_video(link)
