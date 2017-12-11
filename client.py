from PIL import Image
import rgb_encrypter_jumble_2
from collections import Counter
import numpy as np

class Client:

    def __init__(self):
        pass

    def encrypt_image(self, image_name):
        e = Encrypter(image_name)
        e.run()

    def hash_image(self, image_name):
        image = Image.open(image_name)
        image = image.resize((32, 32), Image.ANTIALIAS)
        image = image.convert("L")

        pixels = list(image.getdata())
        #avg = sum(pixels) / len(pixels)

        #bits = "".join(map(lambda pixel: '1' if pixel < avg else '0', pixels))
        #hexadecimal = int(bits, 2).__format__('016x').upper()

        var = np.var(pixels)
        top_freqs = self.get_freqs(pixels)

        prod = long(var * 1000)
        for freq in top_freqs:
            prod = prod * long(freq)
        
        hexadecimal = hex(prod)[2:].upper()
        return hexadecimal

    def get_freqs(self, pixels):
        counter = Counter(pixels)
        most_common = counter.most_common(30)
        most_common = [val for (key, val) in most_common]
        return most_common

#c = Client()
#print(c.hash_image("dog.jpg"))
