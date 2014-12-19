from random import choice, randint
import re
import urllib.request
from urllib.error import HTTPError

image_finder = "imgur.com/(\w+)"
image_finder = re.compile(image_finder)
archive_name = "archived_images.txt"

with open(archive_name, "a+") as archive_file:
    archive_file.write("")


def get_archive():
    global the_archive
    with open(archive_name) as archive_text:
        the_archive = archive_text.read().split("\n")


get_archive()


def proper_urlopen(url):
    headers = {"User-Agent": "Python3.4 Image-Parser"}
    request = urllib.request.Request(url, headers=headers)
    request = urllib.request.urlopen(request)
    text = request.read().decode()
    request.close()
    return text


def proper_subreddit(subreddit_shortcut):
    subreddit_format = "http://www.reddit.com/r/{}"
    return subreddit_format.format(subreddit_shortcut)


def get_json(subreddit):
    text = proper_urlopen(subreddit + (".json" if not subreddit.endswith(".json") else ""))
    return text


def find_images(subreddit):
    sub_json = get_json(subreddit)
    sub_images = image_finder.findall(sub_json)
    return sub_images


def write_image(image_code):
    imgur_format = "http://i.imgur.com/{}.jpg"
    image_url = imgur_format.format(image_code)
    try:
        if image_code in the_archive:
            return 0
        urllib.request.urlretrieve(image_url, image_code + ".jpg")
        return 1
    except HTTPError as error:
        error = str(error)
        if "404" in error:
            print("Image '{}' could not be found".format(image_code))
        else:
            print("Image '{}' failed with exception '{}'".format(image_code, error))
    with open(archive_name, "a+") as archive:
        archive.write(image_code + "\n")
    return 0


def write_images(subreddit, limit=None):
    to_write = find_images(subreddit)
    amount_of_images = 0
    if limit is None or limit > len(to_write):
        limit = len(to_write)
    print("Attempting to write {} images".format(limit))
    for image in to_write[:limit]:
        amount_of_images += write_image(image)
    print("Wrote {} images".format(amount_of_images))


# Here is where the image_parsing part of the scripts stops.
# From now on, these are extra features

def random_sub():
    subs = [
        "pics",
        "aww",
        "httyd",
        "funny",
        "gaming"
    ]
    chosen_sub = choice(subs)
    return proper_subreddit(chosen_sub)


# Merge of extra_kittens
def gen_size():
    h, w = randint(100, 1000), randint(100, 1000)
    return h, w


def gen_name():
    new_name = ""
    for item in range(randint(5, 15)):
        new_name += choice("abcdefghijklmonopqrstuvwxyz")
    return new_name + ".jpg"


def get_kitten_image(path, width, height):
    kitten_format = "http://placekitten.com/g/{}/{}"
    kitten_image_url = kitten_format.format(width, height)
    urllib.request.urlretrieve(kitten_image_url, path)
