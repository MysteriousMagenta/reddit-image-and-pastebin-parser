from time import time
import urllib.request
import re
from random import choice
# Thinking of rewriting this

imagefilter = re.compile("imgur.com/(\w+)")
get_sub = re.compile("/r/(.*?)/?(?:new|top|controversial|hot)?/?(?:\.json)")
heads = {"User-Agent": "Python3.4 Reddit Image Parser"}
filename = "already_archived.txt"
with open(filename, "a+") as image_file:
    image_file.write("")
def archive():
    codes = []
    with open(filename) as image_file:
        for line in image_file:
            codes.append(line.strip())
    return codes

archived = archive()

def properurl(url, string_it=True):
    request = urllib.request.Request(url, headers=heads)
    data = urllib.request.urlopen(request)
    text = data.read()
    data.close()
    if string_it:
        text = str(text)
    return text

def getRedditImages(url):
    images = imagefilter.findall(properurl(url))
    images = [x for x in images if len(x.strip()) != 1 or x != "gallery"]
    return set(images) 

def add_to_file(code):
    if code in archived:
        return False
    with open(filename, "a+") as image_file:
        image_file.write(code + "\n")
    return True
            
def main(url, verbose=True):
    imagecount = 0
    start = time()
    sub = get_sub.findall(url)[0]
    if verbose:
        print("Searching in /r/" + sub)
        print("Querying reddit...")
    try:
        matches = getRedditImages(url)
        if verbose:
            print("Finished with Reddit.")
            print("Found {0} images total.".format(len(matches)))
    except:
        if verbose:
            print("Unvalid url.")
        return
    if verbose:
        print("Adding images...")
    for item in matches:
        if item in archived:
            pass
        else:
            try:
                add_to_file(item)
                url = "http://imgur.com/" + item + ".jpg"
                path = sub + "-" + item +".jpg"
                urllib.request.urlretrieve(url, path)
            except Exception as e:
                if verbose:
                    print("Exception:\n" + str(e))
                    print("{0} failed.".format(item))
            imagecount += 1
    if verbose:
        print("Added images.")
        print("Found {0} new images.".format(imagecount))
        end = time()
        totaltime = int(format(end - start, ".0f"))
        print("Process took {0} second".format(totaltime) + "s" if totaltime > 1 else "")

def randomsub():
    prepare = lambda x: "http://" + x + ".json"
    subs = ["reddit.com/r/aww",
            "reddit.com/r/httyd",
            "reddit.com/r/pics/new",
            "reddit.com/r/wheredidthesodago",
            "reddit.com/r/mylittlepony",
            "reddit.com/r/funny",
            "reddit.com/r/AdviceAnimals"]
    sub = choice(subs)
    return prepare(sub)
    
if __name__ == "__main__":
    main(randomsub())



