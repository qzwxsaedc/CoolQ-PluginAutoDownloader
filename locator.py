import random
import re
import urllib.request as request

from bs4 import BeautifulSoup

import tools as t


def __get_download_file(extension, file_list):
    if extension in file_list:
        if len(file_list[extension]) > 1:
            file_list[extension].sort(key=lambda e: e["id"], reverse=True)
        return file_list[extension][0]
    else:
        return None


def __get_final_download_file(file_list):
    if file_list is None or len(file_list) == 0:
        return None

    ext_list = [".cpk", ".zip", ".rar", ".7z"]
    for ext in ext_list:
        f_dict = __get_download_file(ext, file_list)
        if f_dict:
            f_dict["file_type"] = ext
            return f_dict
    return None


def __get_file_list(var) -> dict:
    if not var:
        return None

    file_list = {}
    for item in var:
        href = item.find("a")["href"]
        file_name = item.find("a").string
        try:
            em = item.find("em").string
            is_old = False
        except AttributeError:
            is_old = True
            tmp = item.find("dd").find_all("p")
            for item2 in tmp:
                if not len(item2.attrs) == 0:
                    em = ""
                    continue
                if not item2.string:
                    continue
                if len(item2.string) > 2:
                    em = item2.string
                    break
                else:
                    em = ""
        attach_id = int(re.match(r"\w+?_?(\d+)_menu", str(item.find("div")["id"])).group(1))
        key = file_name[-4:]
        if key not in file_list:
            file_list[key] = []
            file_list[key].append({
                "href": href,
                "file_name": file_name,
                "is_need_pay": "mod=misc" in href,
                "em": em,
                "id": attach_id,
                "is_old": is_old,
            })
    return file_list


def locator(html: str):
    """定位器入口函数。"""
    soup = BeautifulSoup(html, "html.parser")
    var = soup.find_all(attrs={"class": "di-attach-file"})
    file_list = __get_file_list(var)

    f_dict = __get_final_download_file(file_list)
    return f_dict


def get_element_id(target: dict):
    """一共有两类id: 老版的格式为aid{$id}, 新版的格式为attach_{$id}"""
    if target["is_old"]:
        return "aid{0}".format(target["id"])
    else:
        return "attach_{0}".format(target["id"])
