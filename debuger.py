import http.cookiejar as cj
import random
import urllib.request as request
import os

import tools as t
import locator as lo


def main(__url: str):
    res = request.Request(url=__url, headers={
        "User-Agent": random.choice(t.USER_AGENTS),
        "accept-language": "zh-CN,zh;q=0.9",
    })
    html = request.urlopen(res).read().decode("utf-8")
    print(lo.locator(html))


def _init_():
    __cookie = cj.MozillaCookieJar("cookies_cqp-cc")
    __cookie.load(ignore_discard=True, ignore_expires=True)
    handler = request.HTTPCookieProcessor(__cookie)
    opener = request.build_opener(handler)
    request.install_opener(opener)
    return __cookie


if __name__ == "__main__":
    print(os.path.exists("D:\\python\\auto_downloader\\download\\*.cpk"))
    # pass
    # cookie = _init_()
    #
    # main("https://cqp.cc/t/47355")
    #
    # cookie.save(ignore_discard=True, ignore_expires=True)
