from PIL import Image
import rgb_encrypter_jumble_2

class Client:

    def __init__(self):
        pass

    def encrypt_image(self, image_name):
        e = Encrypter(image_name)
        e.run()

    def hash_image(self, image_name):
        image = Image.open(image_name)
        image = image.resize((8, 8), Image.ANTIALIAS)
        image = image.convert("L")

        pixels = list(image.getdata())
        avg = sum(pixels) / len(pixels)

        bits = "".join(map(lambda pixel: '1' if pixel < avg else '0', pixels))
        hexadecimal = int(bits, 2).__format__('016x').upper()
        
        return hexadecimal

c = Client()
print(c.hash_image("dog.jpg"))
