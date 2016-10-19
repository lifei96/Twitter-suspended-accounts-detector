# -*- coding: utf-8 -*-

import urllib2
import cookielib
import re
import mysql.connector
import variable
import random


def check_suspended(username):
    url = 'https://twitter.com/' + username
    cj = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    req = urllib2.Request(url)
    req.add_header("User-agent", 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/50.0.2661.102 Safari/537.36')
    try:
        response = opener.open(req, timeout=10)
    except urllib2.URLError:
        print('-----404')
        return -1
    data = response.read()

    suspended = re.findall('<title>Twitter / Account Suspended</title>', data)
    if suspended:
        print('-----suspended')
        return 1
    else:
        print('-----not suspended')
        return 0


def get_username_list():
    conn = mysql.connector.connect(port=3306, user=variable.username, password=variable.password,
                                   database='Medium', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT twitter_id FROM twitter"
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()

    queue = []
    for user in result:
        queue.append(user[0])
    for i in range(5):
        random.shuffle(queue)
    return queue


def detect():
    username_list = get_username_list()
    for username in username_list:
        print(username)
        suspended = check_suspended(username)
        conn = mysql.connector.connect(port=3306, user=variable.username, password=variable.password,
                                       database='Medium', charset='utf8')
        cur = conn.cursor()
        sql = "UPDATE twitter SET suspended='%s' WHERE twitter_id='%s'" % (suspended, username)
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()


if __name__ == '__main__':
    detect()
