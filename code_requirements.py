import urllib.request


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