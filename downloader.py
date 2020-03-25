# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import sys
import os
import json
import time
import traceback

import CustomException as ce
import tools as t
import locator as lo
import watchdog_file as wd

browser = None
not_first_run = True


# noinspection SpellCheckingInspection
def config(argv: list):
    """不要问我为什么要这么来处理命令行参数。
    好吧确实很乱。"""
    _config = t.__config
    appid_list = []
    if len(argv):
        tips = "请检查参数是否合法。"
        i = 0
        while i < len(argv) - 1:
            i += 1
            if argv[i] == "--no-cache" or argv[i] == "-n":
                _config["no-cache"] = True
                continue
            if argv[i] == "--no-gui" or argv[i] == "-g":
                _config["no-gui"] = True
                continue
            if argv[i] == "--login-by-qq" or argv[i] == "-q":
                _config["login-by-qq"] = True
                continue
            if argv[i] == "-c":
                if t.is_arg(argv[i + 1]):
                    raise ce.NoArgumentException(argv[i])
                i += 1
                _config["cache-path"] = argv[i]
                continue
            if "--cache-path=" in argv[i]:
                _config["cache-path"] = argv[i][13:]
                continue
            if argv[i] == "-d":
                if t.is_arg(argv[i + 1]):
                    raise ce.NoArgumentException(argv[i])
                i += 1
                _config["download-path"] = argv[i]
                continue
            if "--download-path=" in argv[i]:
                _config["cache-path"] = argv[i][16:]
                continue
            if argv[i] == "-e":
                if t.is_arg(argv[i + 1]):
                    raise ce.NoArgumentException(argv[i])
                i += 1
                _config["email"] = argv[i]
                continue
            if "--email=" in argv[i]:
                _config["email"] = argv[i][8:]
                continue
            if argv[i] == "-p":
                if t.is_arg(argv[i + 1]):
                    raise ce.NoArgumentException(argv[i])
                i += 1
                _config["password"] = argv[i]
                continue
            if "--password=" in argv[i]:
                _config["password"] = argv[i][11:]
                continue
            if argv[i] == "--appid" or argv[i] == "-a":
                if t.is_arg(argv[i + 1]):
                    raise ce.NoArgumentException(argv[i])
                i += 1
                for item in argv[i].split(","):
                    if item is not None and item != "":
                        appid_list.append(item)
                continue
            if argv[i] == "--help" or argv[i] == "-h":
                print(t.help_info)
                sys.exit(0)
            if argv[i] == "--version" or argv[i] == "-v":
                print(t.version_info)
                sys.exit(0)
            raise ce.UnknownArgumentException(argv[i])
    else:
        tips = "请检查配置文件是否合法。"
        try:
            _config = json.load(open("./downloader_config.json"))
        except Exception:
            json.dump(_config, open("./downloader_config.json", "w"), indent=4)
            raise ce.AnotherException(traceback.format_exc())

    if _config["no-cache"] and (_config["email"] == "" or _config["password"] == "") and not _config["login-by-qq"]:
        raise ce.InvalidCompoundException("禁用缓存时必须填写用户名和密码，或启用通过QQ登录。" + tips)

    if not (_config["email"] == "" and _config["password"] == "") and not_first_run:
        _config["no-cache"] = True

    if _config["login-by-qq"]:
        _config["no-cache"] = True
        _config["email"] = ""
        _config["password"] = ""

    if _config["cache-path"] == "":
        raise ce.InvalidPathException("缓存", tips)

    if _config["download-path"] == "":
        raise ce.InvalidPathException("下载", tips)

    if not os.path.exists(_config["cache-path"]):
        try:
            os.makedirs(os.path.join(t.cache_path(), "download_cache"))
        except Exception:
            raise ce.CannotCreatePathException("缓存", traceback.format_exc())

    if not os.path.exists(_config["download-path"]):
        try:
            os.makedirs(_config["download-path"])
        except Exception:
            raise ce.CannotCreatePathException("下载", traceback.format_exc())
    try:
        json.dump(_config, open("./downloader_config.json", "w"), indent=4)
    except Exception:
        raise ce.AnotherException(traceback.format_exc())
    t.__config = _config
    return appid_list


def main(argv: list):
    global browser

    appid_list = config(argv)
    os.removedirs(os.path.join(t.cache_path(), "download_cache"))
    os.makedirs(os.path.join(t.cache_path(), "download_cache"))
    print("参数已载入。")
    options = webdriver.ChromeOptions()

    options.add_argument("--user-data-dir=" + t.__config["cache-path"])
    options.add_argument('disable-infobars')
    options.add_argument('log-level=3')

    if t.__config["no-gui"]:
        options.add_argument("--headless")  # headless模式，没有浏览器窗口
        options.add_argument("--disable-gpu")  # 提高定位精度

    if t.__config["no-cache"]:
        options.add_argument('--incognito')  # 无痕隐身模式
        options.add_argument("disable-cache")  # 禁用缓存

    options.add_experimental_option("prefs", {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": os.path.abspath(os.path.join(t.cache_path(), "download_cache"))
    })

    print("正在初始化浏览器...")
    browser = webdriver.Chrome(options=options)
    print("正在初始化...")
    browser.implicitly_wait(2)  # 2s的隐式延迟
    if (not t.__config["no-cache"]) and not_first_run:
        browser.get("https://cqp.cc/")
        if t.is_element_exist_by_class_name(browser, "di-lic"):
            print("你好像并没有登录账号。先登录账号后再操作罢。1s后将自动跳转至登录界面。")
            time.sleep(1)
            browser.get("https://cqp.me/login?referer=connect%3Fr%3Dhttps%253A%252F%252Fcqp.cc%252F")
            WebDriverWait(browser, 500).until(ec.url_matches(r'^https://cqp\.cc/$'))
    else:
        if t.__config["login-by-qq"]:
            browser.get("https://cqp.me/login?referer=connect%3Fr%3Dhttps%253A%252F%252Fcqp.cc%252F")
            browser.find_element_by_class_name("bind-qq").click()
            WebDriverWait(browser, 500).until(ec.url_matches(r"^https://cqp\.cc/$"))
        else:
            browser.get("https://cqp.me/login?referer=connect%3Fr%3Dhttps%253A%252F%252Fcqp.cc%252F")

            browser.find_element_by_class_name("form-control").send_keys(t.__config["email"])
            browser.find_element_by_class_name("btn-primary").click()
            if t.is_element_exist_by_class_name(browser, "alert-danger"):
                err_str = str(browser.find_element_by_class_name("alert-danger").text)
                raise ce.LoginFailedException(err_str[0:err_str.rfind("。") + 1])

            browser.find_element_by_class_name("form-control").send_keys(t.__config["password"])
            browser.find_element_by_class_name("btn-primary").click()
            if t.is_element_exist_by_class_name(browser, "alert-danger"):
                err_str = str(browser.find_element_by_class_name("alert-danger").text)
                raise ce.LoginFailedException(err_str.replace("找回密码", "") + "请确认密码是否填写正确。")

    if t.is_element_exist_by_class_name(browser, "di-lic"):
        sys.stderr.write("登录失败。请将以下内容与浏览器界面一并反馈给开发者: ")
        raise ce.CustomBaseException(prefix="INFO", arg="di-lic exists: True.", code=100,
                                     addition=traceback.format_exc())

    print("登录成功。")
    err_list = {"appid": [], "thread": []}
    for appid in appid_list:
        try:
            print("工作中: " + appid)
            browser.get("https://cqp.cc/b/app")
            WebDriverWait(browser, 5).until(ec.visibility_of(browser.find_element_by_name("searchoption[11][value]")))
            browser.find_element_by_name("searchoption[11][value]").send_keys(appid)
            browser.find_element_by_name("searchsortsubmit").click()

            print("正在定位文件中...")
            target = lo.locator(browser.page_source)
            if "cqp.cc/forum.php" in browser.current_url:
                print("通过appid搜索对应帖子失败：\n\t可能为错误的appid或有多个帖子拥有相同的appid。\n\t发生错误的appid: " + appid)
                continue
            if not target:
                raise ce.NoValidFileWarning(url)
            print("定位成功。")
            is_need_pay = target["is_need_pay"]
            if is_need_pay:
                url = "https://cqp.cc" + target["href"]
                browser.get(url)
                browser.find_element_by_name("paysubmit").click()
                time.sleep(5)
                pass
            else:
                element_id = lo.get_element_id(target)
                btn = browser.find_element_by_id(element_id)
                if not target["is_old"]:
                    btn = btn.find_element_by_tag_name("a")
                print(btn.text)
                btn.click()
            use = wd.WatchDog(target["file_name"], os.path.join(t.__config["cache-path"], "download_cache")).get_interrupt()
            if not use:
                raise ce.NoValidFileWarning()
            print(appid + " : 下载完成。")
            with open(os.path.join(t.download_path(), target["file_name"]), "wb") as fout:
                with open(os.path.join(t.cache_path(), "download_cache", target["file_name"]), "rb") as fin:
                    fout.write(fin.read())
            os.remove(os.path.join(t.cache_path(), "download_cache", target["file_name"]))
            time.sleep(5)
        except ce.NoValidFileWarning as w:
            print(w)


    print("任务全部完成。")
    if err_list["appid"] and err_list["thread"]:
        print("错误的任务列表:")
        if err_list["appid"]:
            print("\tappid:")
            for item in err_list["appid"]:
                print("\t\t" + item)
        if err_list["thread"]:
            print("\t帖子地址:")
            for item in err_list["thread"]:
                print("\t\t" + item)
    print("5s后自动关闭.")
    time.sleep(5)
    browser.close()
    browser = None


if __name__ == "__main__":
    print(t.always_show)
    not_first_run = os.path.exists("./downloader_config.json")
    try:
        main(sys.argv)
    except ce.CustomBaseException as e:
        print(e)
        print("发生错误。退出。")
        if browser:
            browser.close()
        pass
    except Exception:
        print(traceback.format_exc())
        print("发生错误。退出。")
        if browser:
            browser.close()
