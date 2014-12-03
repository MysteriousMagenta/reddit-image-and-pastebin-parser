
import urllib.request
import re

# Failsafe to make sure the file exists.
with open("already_read.txt", "a+") as already_read:
    already_read.write("")
heads = {"User-Agent":"Python3.4 Reddit/Pastebin Parser 0.1"}
code_query = re.compile(r"pastebin.com/(\w+)")
def already_added(code):
    with open("already_read.txt") as code_file:
        for line in code_file:
            if line.strip().strip("\n") == code:
                return True
    return False
def get_codes(section="new"):
    url = "http://www.reddit.com/r/learnpython/" + section + "/.json"
    request = urllib.request.Request(url, headers=heads)
    data = urllib.request.urlopen(request)
    text = data.read()
    text = str(text)
    links = set(code_query.findall(text))
    return links

def write_pastebin(code):
    if already_added(code):
        print("code {0} was found, but was already copied.".format(code))
        return True
    else:
        print("code {0} was found and is new, and is being written.".format(code))
    with open("already_read.txt", "a") as code_file:
        code_file.write(code + "\n")
    url = "http://pastebin.com/raw.php?i=" + code
    request = urllib.request.Request(url, headers=heads)
    data = urllib.request.urlopen(request)
    text = data.read().decode("utf-8")
    text = str(text)
    with open(code + ".txt", "w") as file:
            file.write("# " + "pastebin.com/" + code + "\n")
    with open(code + ".txt", "a") as file:
            file.write(text)
    return text

def write_all(sub="new"):
    codes = get_codes(sub)
    codes_new = [x for x in codes if not already_added(x)]
    for pastebin in codes:
        print("Trying connection...")
        write_pastebin(pastebin)
        print("Connection got.")
    return codes_new

def main():
    new = write_all()
    print("New pastebins: ")
    if len(new) == 0:
        print("Nothing.")
    else:
        for item in new:
            print(item)
            
if __name__ == "__main__":
    from time import sleep
    while True:
        main()
        print("-"*10)
        sleep(60*5)

