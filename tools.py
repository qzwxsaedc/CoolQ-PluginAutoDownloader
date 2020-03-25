# -*- coding: UTF-8 -*-
from selenium import webdriver
import os

def __ver__():
    return "1.0.5.5"


def __author__():
    return "Skeleton_321"


__config = {
    "no-cache": False,
    "no-gui": False,
    "login-by-qq": False,
    "cache-path": "./cache",
    "download-path": "./download",
    "email": "",
    "password": "",
}

arg_list = [
    "--no-cache", "-n",
    "--no-gui", "-g",
    "--login-by-qq", "-q",
    "--cache-path=", "-c",
    "--download-path=", "-d",
    "--email=", "-e",
    "--password=", "-p",
    "--help", "-h",
    "--version", "-v",
]

always_show = '''
#########################################################################################
            *请不要频繁使用本工具下载文件，为了你的cq币，也是为了你的账号*
              *频繁的操作有可能会导致封号，所以建议使用频率为一天一次。*
                      *那为什么不试试神奇的自动更新提醒插件呢*
###############################自动化插件下载工具 帮助信息###############################
本工具目前仅能从命令行进行加载(UI?在写了在写了)。
目前暂不支持从重复appid的帖子中下载文件的功能。
如果帖子中有多个文件，本工具将自动下载可能为插件的最新文件。
tips:
    0.如果不知道该如何使用，要不要试试神奇的.\\pladownloader.exe --help呢。
      (非Windows系统下为./pladownloader --help)
    1.--no-cache参数的功能为开启chrome/chromium的隐身模式，由于文件下载的需要，缓存目录总是
      会创建的。
    2.允许的最少参数数量为1个，即--appid。
    3.本工具通过webdriver驱动，所以理论上可以通过替换webdriver来支持不同版本的**chrome**和
      **chromium**浏览器(ff用户落泪)。考虑到大部分酷Q用户都拥有chromium 63.0.3237.0 32位，
      所以默认会使用这个版本的webdriver。
    4.第一次启动建议使用--email和--password参数，即通过邮箱登录。
      QQ登录没有经过测试，不敢保证能够正常工作。
    5.由于没有很好的测试，所以暂不建议使用--no-gui参数。如果使用该参数导致bug请反馈。
    6.不建议使用Ctrl-C强行停止，可能会出现一些奇怪的bug。
    7.最开始会出现长时间的空白页的状态(不知道为啥，如果有知道的请务必告知)，此时建议等待而
      不是刷新页面。
'''

help_info = '''
###############################自动化插件下载工具 使用方法###############################
.\\pladownloader.exe [[--no-cache|-n] | [--no-gui|-g] | [--login-by-qq|-q]] |
                     [[--cache-path={$path}|-c {$path}] |
                     [[--download-path={$path}|-d {$path}] |
                     [--email={$email}|-e {$email}] |
                     [--password={password}|-p {password}] |
                     [[--help|-h]|[--version|-v]]
                     [--appid|-a] {$appid_or_list}
###############################自动化插件下载工具 可用参数###############################
--no-cache       -n: 禁用缓存。主要用于自动登录。使用该参数时必须传入email和password参数。
--no-gui         -g: 禁用浏览器窗口显示。
--login-by-qq    -q: 通过绑定的QQ号登录。使用本参数时将自动禁用缓存并不适用邮箱登录，
                     并自动打开登录页面。
--cache-path     -c: 设置缓存文件目录。如果目录不存在将自动创建文件夹。
                     支持相对和绝对路径，默认值为./cache。
--download-path  -d: 设置插件下载目录。如果目录不存在将自动创建文件夹。
                     支持相对和绝对路径，默认值为./download。
--email          -e: 设置邮箱。必须和下一条参数同时使用。将自动禁用缓存。
--password       -p: 设置密码。必须和上一条参数同时使用。
--appid          -a: 传入需要下载更新的appid，支持批量输入，每个appid间用逗号分隔。
                     例如: --appid com.example.demo.api是合法的输入。
--help           -h: 显示帮助信息。
--version        -v: 显示版本号和作者联系信息。
########################################################################################
'''

version_info = '''
当前版本号：{0}
作者：      {1}
论坛：      https://cqp.cc/
'''.format(__ver__(), __author__())

USER_AGENTS = [
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 "
    "Safari/535.11",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; "
    ".NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 "
    "Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 "
    "LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR "
    "3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X "
    "MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12 "
]

_cookie_dist = {}


def is_arg(arg):
    for item in arg_list:
        if item in arg:
            return True
    return False


def download_path():
    return os.path.abspath(__config["download-path"])


def cache_path():
    return os.path.abspath(__config["cache-path"])


def is_element_exist_by_class_name(browser, element):
    try:
        browser.find_element_by_class_name(element)
        return True
    except:
        return False
