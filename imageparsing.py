from time import time
import urllib.request
import re

imagefilter = re.compile("imgur.com/(\w+)")
heads = {"User-Agent": "Python3.4 Reddit Image Parser"}
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

def archive(code):
    filename = "already_archived.txt"
    with open(filename, "a+") as image_file:
        image_file.seek(0)
        for line in image_file:
            if len(re.findall(code, line)) != 0:
                return False
        image_file.write(code + "\n")
        return True
            
def main(url, matches=None, verbose=True):
    imagecount = 0
    start = time()
    get_sub = re.compile("/r/(.*?)/?(?:new|top|controversial|hot)?/?(?:\.json)")
    sub = get_sub.findall(url)[0]
    if matches == None:
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
        if not archive(item):
            pass
        else:
            imagecount += 1
            try:
                url = "http://www.imgur.com/" + item + ".jpg"
                path = sub + "-" + item +".jpg"
                urllib.request.urlretrieve(url, path)
            except Exception as e:
                if verbose:
                    print(str(e))
                    print("{0} failed.".format(item))
    if verbose:
        print("Added images.")
        print("Found {0} new images.".format(imagecount))
        end = time()
        totaltime = int(format(end - start, ".0f"))
        print("Process took {0} second".format(totaltime) + "s" if totaltime > 1 else "")


from random import choice
def randomsub():
    prepare = lambda x: "http://" + x + ".json"
    subs = ["reddit.com/r/aww",
            "reddit.com/r/httyd",
            "reddit.com/r/pics/new",
            "reddit.com/r/wheredidthesodago",
            "reddit.com/r/mylittlepony",
            "reddit.com/r/funny",
            "reddit.com/r/AdviceAnimals"
            ]
    sub = choice(subs)
    return prepare(sub)
    
if __name__ == "__main__":
    main(randomsub())



