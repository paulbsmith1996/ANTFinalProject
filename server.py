from PIL import Image
import os
import numpy as np
from collections import Counter

class Server:

    # Holds the name of the directory where the illegal images are stored
    IMAGES_DIR = "illegal_images/"

    # Minimal Hamming distance a hash must be from all illegal hashes to be considered
    # a legal hash
    THRESHOLD = 4

    # The number of pixel counts used to generate our hash
    TOP_FREQ_NUM = 30

    # Server holds a list of illegal hashes, based on given illegal images. Server also
    # stores encrypted versions of legal images uploaded by client
    def __init__(self):
        self.illegal_hashes = []
        self.load_illegal_images()
        self.stored_images = []

    # Generate the list of illegal hashes, based on the illegal images
    def load_illegal_images(self):
        file_names = os.listdir(Server.IMAGES_DIR)
        for file_name in file_names:
            if file_name[len(file_name) - 4:] == ".png": # Make sure file is a png
                self.illegal_hashes.append(self.hash_image(Image.open(Server.IMAGES_DIR + file_name)))

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
        most_common = counter.most_common(30)
        most_common = [val for (key, val) in most_common]
        return most_common

    # Verifies that the passed hash is the hash of a legal image
    def check_legal(self, test_image_hash):

        for hash in self.illegal_hashes:

            # Compute the Hamming distance between the passed hash and the
            # hash of the illegal image
            distance = abs(len(hash) - len(test_image_hash))
            for i in range(  min( len(hash), len(test_image_hash) ) - 1  ):
                if int(hash[i], 16) - int(test_image_hash[i], 16) != 0:
                    distance = distance + 1

            if(distance < Server.THRESHOLD): return False
                    
        return True

    # Stores the image if it has a legal hash. Otherwise, inform the user that the
    # image is illegal and reject
    def upload_image(self, image_name):
        
        # Get the image stored in the passed location
        image = Image.open(image_name)

        # Compute the hash of the image
        image_hash = self.hash_image(image)

        # Store if legal, reject if not
        if image_hash not in self.illegal_hashes:
            self.stored_images.append((image_hash, image))
            print "Successfully uploaded " + image_name
        else:
            print "Failed to upload illegal image " + image_name
