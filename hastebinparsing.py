import re
import code_requirements
import json

hastebin_format = "http://hastebin.com/documents/{}"
filename = "already_read_hastebins.txt"
hastebin_finder = "hastebin.com/(\w+)"
hastebin_finder = re.compile(hastebin_finder)
with open(filename, "a+") as haste_archive:
    haste_archive.write("")


def find_hastebins(url, is_reddit=True):
    if is_reddit:
        url = code_requirements.proper_subreddit(url)
        url = code_requirements.get_json(url)
    else:
        url = code_requirements.proper_urlopen(url)
    return set(hastebin_finder.findall(url))


def get_hastebins():
    the_archive = []
    with open(filename) as hastebin_archive:
        for line in hastebin_archive:
            the_archive.append(line.strip())
    return the_archive
archive = get_hastebins()


def get_json(hastebin_id):
    json_raw = code_requirements.proper_urlopen(hastebin_format.format(hastebin_id))
    json_dict = json.loads(json_raw)
    return json_dict


def get_contents(hastebin_id):
    hastebin_dict = get_json(hastebin_id)
    hastebin_content = hastebin_dict["data"]
    return hastebin_content


def write_hastebin(hastebin_id, extension=".py"):
    if hastebin_id in archive:
        return
    hastebin_content = get_contents(hastebin_id)
    with open(filename, "a+") as hastebin_archive:
        hastebin_archive.write(hastebin_id + "\n")
    with open(hastebin_id + extension, "w") as hastebin_file:
        hastebin_file.write(hastebin_content)
