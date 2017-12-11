from PIL import Image
import os
from client import Client
import numpy as np
from collections import Counter

class Server:

    IMAGES_DIR = "illegal_images/"
    THRESHOLD = 4

    def __init__(self):
        self.hashes = []
        self.load_illegal_images()
        self.stored_images = []

    def load_illegal_images(self):
        file_names = os.listdir(Server.IMAGES_DIR)
        for file_name in file_names:
            self.hashes.append(self.hash_image(file_name))

    """
    def hash_image(self, image_name):
        image = Image.open(Server.IMAGES_DIR + image_name)
        image = image.resize((8, 8), Image.ANTIALIAS)
        image = image.convert("L")

        pixels = list(image.getdata())
        avg = sum(pixels) / len(pixels)

        bits = "".join(map(lambda pixel: '1' if pixel < avg else '0', pixels))
        hexadecimal = int(bits, 2).__format__('016x').upper()

        return hexadecimal
    """

    def hash_image(self, image_name):
        image = Image.open(Server.IMAGES_DIR + image_name)
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

    def check_legal(self, test_image_hash):

        #test_image_hash_bin = test_image_hash

        for hash in self.hashes:
            #hash_bin = hash, 16)

            distance = abs(len(hash) - len(test_image_hash))

            for i in range(  min( len(hash), len(test_image_hash) ) - 1  ):
                if int(hash[i], 16) - int(test_image_hash[i], 16) != 0:
                    distance = distance + 1

            if(distance < Server.THRESHOLD): return False
                    
        return True

