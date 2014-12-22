import code_requirements
import urllib.request
import re
import json
import os
original_dir = os.getcwd()
gist_format = "https://api.github.com/gists/{}"

gist_finder = "gist.github.com/\w+/(\w+)"
gist_finder = re.compile(gist_finder)

gist_content_finder = '"content":\s*"(.*?)"'
gist_name_finder = '"filename":\s*"(.*?)"'

gist_content_finder = re.compile(gist_content_finder)
gist_name_finder = re.compile(gist_name_finder)

filename = "already_read_gists.txt"
with open(filename, "a+") as gist_archive_file:
    gist_archive_file.write("")


def get_archived_gists():
    archive = []
    with open(filename) as gist_archive:
        for line in gist_archive:
            archive.append(line.strip())
    return archive
archived_gists = get_archived_gists()


def find_gists(url, is_reddit=True):
    if is_reddit:
        url = code_requirements.proper_subreddit(url)
        url = code_requirements.get_json(url)
    else:
        url = code_requirements.proper_urlopen(url)
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
        with open(filename, "a+") as gist_archive:
            gist_archive.write(gist + "\n")


def write_gists(url, is_reddit=True):
    gist_list = find_gists(url, is_reddit)
    for item in gist_list:
        write_gist(item)
        os.chdir(original_dir)