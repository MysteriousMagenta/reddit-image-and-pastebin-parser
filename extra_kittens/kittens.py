import urllib.request
import random
import string

width = random.randrange(100, 1000)
height = random.randrange(100, 1000)
url = "http://www.placekitten.com/g/" + str(width) + "/" + str(height)
image = urllib.request.urlopen(url).read()
filename = ""
for item in range(random.randint(10, 25)): filename += random.choice(string.ascii_letters)
with open(filename + ".png", "wb") as kitten:
    kitten.write(image)
