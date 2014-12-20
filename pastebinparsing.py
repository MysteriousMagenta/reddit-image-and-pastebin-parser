import urllib.request
import re
pastebin_finder = re.compile("pastebin.com/(\w+)")
pastebin_raw_format = "http://pastebin.com/raw.php?i={}"
file_name = "already_read.txt"


def get_pastebins():
    global read_pastebins
    read_pastebins = []
    with open(file_name, "a+") as pastebin_file:
        pastebin_file.write("")
    with open(file_name) as pastebin_file:
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


def write_pastebin(code):
    if code in read_pastebins:
        return
    with open(file_name, "a+") as pastebin_file:
        pastebin_file.write(code + "\n")
    pastebin_content = get_raw_pastebin(code)
    with open(code+".txt", "w") as pastebin_file:
        pastebin_file.write(pastebin_content)


def write_pastebins(url, is_reddit=True):
    url_pastebins = find_pastebins(url, is_reddit)
    for item in set(url_pastebins):
        write_pastebin(item)

if __name__ == "__main__":
    reddit_url = proper_subreddit("learnpython")
    write_pastebins(reddit_url)
