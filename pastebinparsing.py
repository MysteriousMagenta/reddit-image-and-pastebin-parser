from code_requirements import *
import re


pastebin_finder = "pastebin.com/(\w+)"
pastebin_finder = re.compile(pastebin_finder)
raw_format = "http://pastebin.com/raw.php?i={}"
filename = "already_read_pastebins.txt"
with open(filename, "a+") as archive:
    archive.write("")


def get_pastebins():
    pastebin_archive = []
    with open(filename) as pastebin_file:
        for line in pastebin_file:
            pastebin_archive.append(line.strip())
    return pastebin_archive
read_pastebins = get_pastebins()


def find_pastebins(url, is_reddit=True):
    if is_reddit:
        url = proper_subreddit(url)
        url = get_json(url)
    else:
        url = proper_urlopen(url)
    return pastebin_finder.findall(url)


def get_raw_pastebin(code):
    pastebin_link = raw_format.format(code)
    pastebin_text = proper_urlopen(pastebin_link)
    return pastebin_text


def write_pastebin(code, extension=".py"):
    if code in read_pastebins:
        return
    with open(filename, "a+") as pastebin_file:
        pastebin_file.write(code + "\n")
    pastebin_content = get_raw_pastebin(code)
    with open(code+extension, "w") as pastebin_file:
        pastebin_file.write(pastebin_content)


def write_pastebins(url, is_reddit=True):
    url_pastebins = find_pastebins(url, is_reddit)
    for item in set(url_pastebins):
        write_pastebin(item)