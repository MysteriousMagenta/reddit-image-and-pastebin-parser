import urllib.request
import re
import json
import os
original_dir = os.getcwd()

pastebin_raw_format = "http://pastebin.com/raw.php?i={}"
gist_format = "https://api.github.com/gists/{}"

pastebin_finder = "pastebin.com/(\w+)"
pastebin_finder = re.compile(pastebin_finder)

gist_finder = "gist.github.com/\w+/(\w+)"
gist_finder = re.compile(gist_finder)

gist_content_finder = '"content":\s*"(.*?)"'
gist_name_finder = '"filename":\s*"(.*?)"'

gist_content_finder = re.compile(gist_content_finder)
gist_name_finder = re.compile(gist_name_finder)

file_name_pastebin = "already_read_pastebins.txt"
file_name_gist = "already_read_gists.txt"

with open(file_name_gist, "a+") as gist_archive_file:
    gist_archive_file.write("")
with open(file_name_pastebin, "a+") as pastebin_archive_file:
    pastebin_archive_file.write("")


def get_pastebins():
    global read_pastebins
    read_pastebins = []
    with open(file_name_pastebin) as pastebin_file:
        for line in pastebin_file:
            read_pastebins.append(line.strip())
    return read_pastebins
get_pastebins()


def get_json(subreddit):
    if not subreddit.endswith(".json"):
        subreddit += ".json"
    subreddit_json = proper_urlopen(subreddit)
    return subreddit_json


def proper_subreddit(shortcut):
    if not shortcut.startswith("http://reddit.com/r/") or shortcut.startswith("http://www.reddit.com/r/"):
        return "http://reddit.com/r/{}".format(shortcut)
    return shortcut


def proper_urlopen(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Reddit Python3.4 Pastebin Parser"})
    request = urllib.request.urlopen(request)
    text = request.read().decode()
    request.close()
    return text

# Pastebin


def find_pastebins(url, is_reddit=True):
    if is_reddit:
        url = proper_subreddit(url)
        url = get_json(url)
    else:
        url = proper_urlopen(url)
    return pastebin_finder.findall(url)


def get_raw_pastebin(code):
    pastebin_link = pastebin_raw_format.format(code)
    pastebin_text = proper_urlopen(pastebin_link)
    return pastebin_text


def write_pastebin(code, extension=".py"):
    if code in read_pastebins:
        return
    with open(file_name_pastebin, "a+") as pastebin_file:
        pastebin_file.write(code + "\n")
    pastebin_content = get_raw_pastebin(code)
    with open(code+extension, "w") as pastebin_file:
        pastebin_file.write(pastebin_content)


def write_pastebins(url, is_reddit=True):
    url_pastebins = find_pastebins(url, is_reddit)
    for item in set(url_pastebins):
        write_pastebin(item)


def get_archived_gists():
    archive = []
    with open(file_name_gist) as gist_archive:
        for line in gist_archive:
            archive.append(line.strip())
    return archive
archived_gists = get_archived_gists()


def find_gists(url, is_reddit=True):
    if is_reddit:
        url = proper_subreddit(url)
        url = get_json(url)
    else:
        url = proper_urlopen(url)
    return list(set(gist_finder.findall(url)))


def get_gist_dict(gist_id):
    gist_url = gist_format.format(gist_id)
    gist_json = urllib.request.urlopen(gist_url).read().decode()
    gist_dict = json.loads(gist_json)
    return gist_dict


def get_gist_files(gist_id):
    gist_dict = get_gist_dict(gist_id)
    gist_files = gist_dict["files"]
    gist_files_filtered = {}
    for item in gist_files:
        if item not in archived_gists:
            gist_files_filtered[item] = gist_files[item]
    return gist_files_filtered


def write_gist(gist_id):
    gist_files = get_gist_files(gist_id)
    if len(gist_files) > 1 and len(gist_files) >= 1:
        try:
            os.mkdir(gist_id)
        except FileExistsError:
            pass
        os.chdir(gist_id)
    for gist in gist_files:
        if gist in archived_gists:
            continue
        gist_dict = gist_files[gist]
        gist_content = gist_dict["content"]
        with open(gist, "w") as gist_file:
            gist_file.write(gist_content)
    os.chdir(original_dir)
    for gist in gist_files:
        with open(file_name_gist, "a+") as gist_archive:
            gist_archive.write(gist + "\n")


def write_gists(url, is_reddit=True):
    gist_list = find_gists(url, is_reddit)
    for item in gist_list:
        write_gist(item)
        os.chdir(original_dir)