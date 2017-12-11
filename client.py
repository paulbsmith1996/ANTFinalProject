from PIL import Image
from rgb_encrypter_jumble_2 import Encrypter
from image_decrypter_3 import Decrypter
from collections import Counter
import numpy as np
from server import Server

class Client:

    # The number of pixel counts used to generate our hash
    TOP_FREQ_NUM = 30

    # A client keeps track of keys and matrices used to encrypt each image.
    # These become dictionaries keyed by image hashes
    def __init__(self):
        self.keys = []
        self.matrices = []

    # Uses the rgb encrypter to encrypt the image with the given name
    def encrypt_image(self, image_name):
        e = Encrypter(image_name)
        key, P_1, P_2 = e.run()
        image_hash = self.hash_image(Image.open(image_name))
        self.keys.append((image_hash, key))
        self.matrices.append((image_hash, (P_1, P_2)))

    # Computes the hash function, invariant under our encryption scheme
    def hash_image(self, image):
        pixels = list(image.getdata())

        top_freqs = self.get_freqs(pixels)

        # Hash is the product of the highest pixel frequencies
        prod = 1
        for freq in top_freqs:
            prod = prod * long(freq)
        
        hexadecimal = hex(prod)[2:].upper()
        return hexadecimal

    # Returns the counts of the most frequently occuring pixels
    def get_freqs(self, pixels):
        counter = Counter(pixels)
        most_common = counter.most_common(Client.TOP_FREQ_NUM)
        most_common = [val for (key, val) in most_common]
        return most_common

    # Attempt to upload the given image to the server
    def upload_image(self, image_name, server):
        server.upload_image(image_name)

    # Retrieve the encrypted images stored on the server and decrypt using
    # appropriate key and permutation matrices
    def retrieve_images(self, server):
        encrypted_images = server.stored_images

        # Create a dictionary for the keys and matrices, for simple lookup expression
        key_dict = dict(self.keys)
        mat_dict = dict(self.matrices)

        for hash, encrypted_image in encrypted_images:
            d = Decrypter(encrypted_image)

            # Retrieve key and matrices
            key = key_dict[hash]
            P_1, P_2 = mat_dict[hash]

            # Decrypt and display pictures stored by server
            unjumbled_pixels, decrypted_pixels = d.gen_decrypted_image(d.pixels, key, P_1, P_2)
            d.display_results(decrypted_pixels)
            
