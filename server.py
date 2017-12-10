from PIL import Image
import os
from client import Client

class Server:

    IMAGES_DIR = "illegal_images/"
    THRESHOLD = 4

    def __init__(self):
        self.hashes = []
        self.load_illegal_images()
        pass

    def load_illegal_images(self):
        file_names = os.listdir(Server.IMAGES_DIR)
        for file_name in file_names:
            self.hashes.append(self.hash_image(file_name))
        

    def hash_image(self, image_name):
        image = Image.open(image_name)
        image = image.resize((8, 8), Image.ANTIALIAS)
        image = image.convert("L")

        pixels = list(image.getdata())
        avg = sum(pixels) / len(pixels)

        bits = "".join(map(lambda pixel: '1' if pixel < avg else '0', pixels))
        hexadecimal = int(bits, 2).__format__('016x').upper()

        return hexadecimal

    def check_legal(self, test_image_hash):

        test_image_hash_bin = bin(int(test_image_hash, 16))[2:]

        for hash in self.hashes:
            hash_bin = bin(int(hash, 16))[2:]

            distance = abs(len(hash_bin) - len(test_image_hash_bin))

            for i in range(  min( len(hash_bin), len(test_image_hash_bin) )  ):
                if int(hash_bin[i]) - int(test_image_hash_bin[i]) != 0:
                    distance = distance + 1

            if(distance < Server.THRESHOLD): return False
                    
        return True

s = Server()
c = Client()
test_hash = c.hash_image("landscape.jpg")
print (s.check_legal(test_hash))
