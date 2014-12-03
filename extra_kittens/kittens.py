import urllib.request
import random
import string

def genSize():
    width = random.randrange(100, 1000)
    height = random.randrange(100, 1000)
    return width, height

def getImage()
    width, height = genSize()
    url = "http://www.placekitten.com/g/" + str(width) + "/" + str(height)
    img = urllib.request.urlopen(url).read()
    return img

def genTitle():
    filename = ""
    for item in range(5):
        filename += random.choice(string.ascii_letters)
        
def main()
    filename = genTitle()
    image = genImage()
    with open(filename + ".png", "wb") as kitten:
        kitten.write(image)

if __name__ == "__main__":
    main()
