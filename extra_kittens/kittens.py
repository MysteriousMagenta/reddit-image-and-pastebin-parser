import urllib.request
from random import randint, choice
from string import ascii_letters, digits
source = ascii_letters + digits
def genSize():
    width = randint(100, 1000)
    height = randint(100, 1000)
    return width, height

def genTitle(length=randint(5, 10)):
    if not isinstance(length, int):
        print("Length was not an integer.")
        return
    title = ""
    for item in range(length):
        title += choice(source)
    return title + ".jpg"

def getImage():
    width, height = [str(x) for x in genSize()]
    url = "http://placekitten.com/g/" + width + "/" + height
    urllib.request.urlretrieve(url, genTitle())
    return width+"x"+height

def main(amount=10):
    for item in range(amount):
        print(getImage())

if __name__ == "__main__":
    main()
        
    
    
