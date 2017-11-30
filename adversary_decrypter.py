


def decrypt_exp_2(encrypted_rgb, key, inv):
    # Get the index associated to the encrypted pixel                                             
    encrypted_index = rgb_to_index(encrypted_rgb)

    # Find the index associated to the decrypte pixel, using our                                  
    # exponential inverse function                                                                
    decrypted_index = exponentiation((256**3) + 1,
                                     encrypted_index,
                                     inv)

    return index_to_rgb(decrypted_index)


def decrypt_image(encrypted_pixels, key):
    inv = slow_exp_inverse((256**3) + 1, key)

    enc_pix = []
    for pix in encrypted_pixels:
        enc_pix.append((int(pix[0]), int(pix[1]), int(pix[2])))

    return [decrypt_exp_2(pixel, key, inv) for pixel in enc_pix]


def compare_pixels(pixel_list_1, pixel_list_2):
    return None


class Adversary:

    def __init__(self, image_name):

        self.im_width = 0
        self.im_height = 0

        self.image_name = image_name

        self.pixels = self.get_image()


    def run(self):
        

    def get_image(self):

        print "\nGetting image"

        # Get the pixels of a given image and find the pixels we are interested in                
        im = Image.open(self.image_name + "_encrypted" + Encrypter.PNG_EXT)
        pix = im.load()

        self.im_width = im.size[0]
        self.im_height = im.size[1]

        pos_x = [(i * (im.size[0] - 1)) / (self.im_width - 1) for i in range(self.im_width)]
        pos_y = [(i * (im.size[1] - 1)) / (self.im_height - 1) for i in range(self.im_height)]
        positions = list(itertools.product(pos_y, pos_x))

        pixels = [pix[pos[1], pos[0]] for pos in positions]

        return pixels
