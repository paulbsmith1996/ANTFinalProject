"""
This program implements an interesting but likely unsound and expensive 
cryptographic scheme for images. The goal here is to produce make our
image data readable at every level or our encryption protocol: the plain
image should obviously be readable, as should the decrypted image, but
we go a step further and mae the encrypted image readable as well.

This is obviously not recommended for an efficient cryptographic system,
where we would want to utilize standard image encryption algorithms to
minimize our memory usage and time complexity. Our goal is more
mathematical an artistic than antyhing else.

Therefore, we need to develop an encryption scheme that encodes each
pixel's as a readable rgb tuple. We do this by assigning each possible
pixel value to a number in Z_{(256^3)} (we essentially write the pixel's
rgb value as a number base 256). This is a unique encoding for each
possible pixel value. We then work in the group Z_{(256^3 + 1)}*, the
units of the group.

Translation from an "index" to an "rgb" value is implemented below, as
is the reverse operation

We also do not claim that our scheme is secure, as this number is easily
factorized and this factorization can then be used to break our system
quickly, though this is not necessarily obvious for large images.

Dependent on pygame and numpy libraries
"""


# Imports
import itertools
import collections
import pygame
import sys
import numpy as np

from PIL import Image
from time import sleep

from rgb_encrypter_jumble_2 import Encrypter


##--------------------- ENCRYPTION / DECRYPTION FUNCTIONS ---------------------##


# Computes the value of the original pixel, given its encryped associate
# Note that this method is extermely slow, as it brute forces the problem
def decrypt(encrypted_rgb, key):

    # Compute the encrypted pixel's associated index
    encrypted_index = rgb_to_index(encrypted_rgb)
    
    # Find the index associated to the value of the decrypted pixel
    decrypted_index = -1
    for d in range(256 ** 3):
        if(exponentiation((256 ** 3) + 1, d, key) == encrypted_index):
            decrypted_index = d
            print "found a d: " + str(d) + "  " + str(index_to_rgb(d))
            break
            
        # Update progress for sanity
        if d % 1000000 == 0:
            print d
            

    decrypted_rgb = index_to_rgb(decrypted_index)
    return decrypted_rgb



# Much quicker function for computing the original pixel, given its 
# encrypted accociate. Computes the exponential inverse of the passed key
def decrypt_exp(encrypted_rgb, key):

    # Get the index associated to the encrypted pixel 
    encrypted_index = rgb_to_index(encrypted_rgb)

    # Find the index associated to the decrypte pixel, using our
    # exponential inverse function
    decrypted_index = exponentiation((256**3) + 1, 
                                     encrypted_index, 
                                     slow_exp_inverse((256**3) + 1, key))

    return index_to_rgb(decrypted_index)

def decrypt_exp_2(encrypted_rgb, key, inv):
    # Get the index associated to the encrypted pixel 
    encrypted_index = rgb_to_index(encrypted_rgb)

    # Find the index associated to the decrypte pixel, using our
    # exponential inverse function
    decrypted_index = exponentiation((256**3) + 1, 
                                     encrypted_index, 
                                     inv)

    return index_to_rgb(decrypted_index)




##--------------------------- ALGEBRAIC FUNCTIONS ------------------------##


# Computes the exponential inverse of exp in Z_{num}
def slow_exp_inverse(num, exp):

    # Pick a random prime to use our dummy number. Note that the prime
    # must be below (256^3).
    key = 151

    # Test all values to find exponential inverse
    encrypted = exponentiation(num, key, exp)
    i = 2
    while i < num:
        if exponentiation(num, encrypted, i) == key:
            return i

        i = i + 1

    return -1



# Returns g^x (mod n)
def exponentiation(n, g, x):
    total = 1
    a = g

    while(x > 0):
        if(x % 2 == 1): total = total * a
        total = total % n

        a = (a * a) % n
        x = x / 2

    return total


# Computes the inverse of g mod n
def inverse(n, g):
    return exponentiation(n, g, (n-2))


# In theory (though not tested), computes the exponential inverse of
# g mod n such that (x^g)^(g^{-1}) = x (mod n)
def exp_inverse(n, g):
    return inverse(n-1, g)






##--------------------------- UTILITY FUNCTIONS ------------------------##


## ALL FUNCTIONS COMMENTED/EXPLAINED IN ENCRYPTER FILE ##

# Computes the index associated to the passed rgb value. This is an
# element of Z_{256^3 + 1}
def rgb_to_index(rgb):
    # Write tuple as a base 256 number
    return rgb[0] + (rgb[1] * 256) + (rgb[2] * (256 ** 2)) + 1



# Computes the rgb value associated to the passed index. This is a tuple
# of size 3
def index_to_rgb(index):
    new_rgb = []
    new_index = index - 1

    # Compute the rgb values according to the 3 "digits" in index
    for i in range(3):
        new_rgb.append(new_index % 256)
        new_index = new_index / 256

    new_rgb = (new_rgb[0], new_rgb[1], new_rgb[2])
    return new_rgb


def list_to_matrix(list):

    list_len = len(list)
    mat = np.zeros([list_len, list_len])

    for j in range(list_len):
        mat[j, list[j]] =  1

    return mat


def matrix_to_list(mat):

    list = []

    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if(mat[i, j] != 0):
                list.append(j)
                break

    return list



def factorization(num):
    
    factors = []
    cur_factor = 2

    # Loop through all numbers until num is 1
    while(num > 1):
        # Count the number of times the current factor divides num
        factor_count = 0
        while(num % cur_factor == 0):
            num = num / cur_factor
            factor_count = factor_count + 1

        # Add the right number of factors to our list, if any
        if(factor_count > 0):
            for i in range(factor_count):
                factors.append(cur_factor)

        cur_factor = cur_factor + 1

    return factors




#-------------------------------IMAGE LEVEL DECRYPTION----------------------------#

def decrypt_image(encrypted_pixels, key):
    inv = slow_exp_inverse((256**3) + 1, key)

    enc_pix = []
    for pix in encrypted_pixels:
        enc_pix.append((int(pix[0]), int(pix[1]), int(pix[2])))

    return [decrypt_exp_2(pixel, key, inv) for pixel in enc_pix]


def unjumble_image(jumbled_pixels, P_1, P_2):
    
    width = P_1.shape[0]
    height = P_2.shape[0]

    jum_pix = []
    for pix in jumbled_pixels:
        jum_pix.append((int(pix[0]), int(pix[1]), int(pix[2])))

    indices = [rgb_to_index(pixel) for pixel in jumbled_pixels]
    
    inds = np.asarray(indices)

    square_inds = inds.reshape([width, height])

    # The transpose of a permutation matrix is its inverse
    square_inds = (P_1.T).dot(square_inds).dot(P_2.T)

    jumbled_inds = square_inds.reshape([width * height, 1])
    return [index_to_rgb(index) for index in jumbled_inds]
    
    



##--------------------------- EXECUTABLE CODE ------------------------##

class Decrypter:

    def __init__(self, image_name):

        print "Decrypter Started"
        if image_name is None:
            print "Indicate a file to decrypt"
            return 

        self.im_width = 0
        self.im_height = 0
        
        self.image_name = image_name
        self.pixels = self.get_image()

        self.key, self.P_1, self.P_2 = self.load_crypto()

        self.unjumbled_pixels, self.decrypted_pixels = self.gen_decrypted_image(self.pixels, self.key, 
                                                                           self.P_1, self.P_2)

        self.display_results(self.pixels, self.unjumbled_pixels, self.decrypted_pixels)
        


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


    def load_crypto(self):

        print "Getting key"

        key_file = open(self.image_name + Encrypter.KEY_TAG + Encrypter.TXT_EXT)
        key = int(key_file.readline())
        key_file.close()

        print "Getting matrices"

        P_1_list = []
        P_2_list = []

        matrix_file = open(self.image_name + Encrypter.MATRIX_TAG + Encrypter.TXT_EXT)

        second_mat = False

        for line in matrix_file:
            for word in line.split():
        
                if "[" in word and "]" not in word:
                    new_word = word[1:]

                    if(not second_mat):
                        P_1_list.append(int(new_word))
                    else:
                        P_2_list.append(int(new_word))

                elif "]" in word:
                    new_word_1 = word[0:word.find("]")]
                    new_word_2 = word[word.find("[") + 1:]

                    if(not second_mat):
                        P_1_list.append(int(new_word_1))
                        P_2_list.append(int(new_word_2))
                    else:
                        P_2_list.append(int(new_word_1))

                    second_mat = True

                else:
                    new_word = word
                    
                    if(not second_mat):
                        P_1_list.append(int(new_word))
                    else:
                        P_2_list.append(int(new_word))

                        
        matrix_file.close()

        P_1 = list_to_matrix(P_1_list)
        P_2 = list_to_matrix(P_2_list)

        return (key, P_1, P_2)


    def gen_decrypted_image(self, pixels, key, P_1, P_2):
        print "Unjumbling jumbled image"
        unjumbled_pixels = unjumble_image(pixels, P_1, P_2)

        print "Decrypting pixels"
        decrypted_pixels = decrypt_image(unjumbled_pixels, key)

        print "Saving unencrypted Image"
        unjum_pix = np.asarray(decrypted_pixels).reshape([self.im_width, self.im_height, 3])
        im = Image.fromarray(unjum_pix.astype('uint8'))
        im.save(self.image_name + "_decrypted" + Encrypter.JPG_EXT)

        return (unjumbled_pixels, decrypted_pixels)


    def display_results(self, pixels, unjumbled_pixels, decrypted_pixels):
        print "Initializing pygame\n"

        # Boot up a pygame window and adjust size
        pygame.init()
        screen = pygame.display.set_mode((Encrypter.WINDOW_WIDTH, Encrypter.WINDOW_HEIGHT))

        print "\n\nDrawing images"

        # Produce our 3 images: the image on the left will be our "plaintext" image.
        # In the center we have the encrypted image, and on the right we have the 
        # decrypted image
        for i in range(3):
    
            # Keep track of our x and y coordiantes within the image we are displaying
            x = 0
            y = 0

            # Loop through all pixels in our images
            for j in range(len(pixels)):

                # Set the x, y, width, and length of the current pixel we are drawing
                rectCoords = (Encrypter.WIN_OFFSET + i * (Encrypter.IMAGE_WIDTH + Encrypter.WIN_OFFSET) + x, 
                              Encrypter.WIN_OFFSET + y,
                              1, 1)

                # Update our image coordinates correctly
                x = x + 1
                # if(x % SQRT_NUM_PIXELS == 0):
                if(x % self.im_height == 0):
                    x = 0
                    y = y + 1
            
        
                if (i == 0):
                    # We are drawing our original image
                    pygame.draw.rect(screen, pixels[j], rectCoords, 0)
                elif (i == 1):
                    # We are drawing our encypted image
                    pygame.draw.rect(screen, unjumbled_pixels[j], rectCoords, 0)
                elif (i == 2):
                    # We are drawing our decrypted image
                    pygame.draw.rect(screen, decrypted_pixels[j], rectCoords, 0)

            # Update the display once all pixel values in the image have been determined
            pygame.display.update()

        print "Images drawn\n"

        # Continue to pass indefinitely so that pygame does not exit
        sleep(10)
        print "Exiting\n"


if len(sys.argv) > 1:
    d = Decrypter(sys.argv[1])
else:
    d = Decrypter(None)
