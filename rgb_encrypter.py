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
import pygame
import sys
import numpy as np
from PIL import Image




##--------------------- ENCRYPTION / DECRYPTION FUNCTIONS ---------------------##


# Encrypt a pixel's rgb value using the given key
def encrypt(rgb, key):

    # Write your rgb tuple as a number in a sequence of length 256^3 
    index = rgb_to_index(rgb)

    # Find the index of your encrypted pixel in your sequence
    new_index = exponentiation((256 ** 3) + 1, index, key)

    # Verify that the new index obtained is not 0
    if(new_index == 0):
        print "new_index is 0"
        return

    # Find the rgb value associated to the new (encrypted) index
    new_rgb = index_to_rgb(new_index)

    return new_rgb



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


# Returns a list representation of the prime factors of num
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





##--------------------------- EXECUTABLE CODE ------------------------##

IMAGE_NAME = "dog.jpg"

# Set constants for graphics in pygame
WIN_OFFSET = 10

IMAGE_WIDTH = 450
IMAGE_HEIGHT = 500

WINDOW_WIDTH = (3 * IMAGE_WIDTH) + (4 * WIN_OFFSET)
WINDOW_HEIGHT = IMAGE_HEIGHT + 2 * WIN_OFFSET

# Determine the number of pixels in our desired image
NUM_PIXELS = 202500
SQRT_NUM_PIXELS = int(NUM_PIXELS ** 0.5)

# Compute the width and height of each "pixel" in our image
RECT_WIDTH = IMAGE_WIDTH / SQRT_NUM_PIXELS
RECT_HEIGHT = IMAGE_HEIGHT / SQRT_NUM_PIXELS


# Boot up a pygame window and adjust size
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Key selected randomly. Can pick any prime in Z_{(256^3) + 1}
key = 24421

# Get the pixels of a given image and find the pixels we are interested in
im = Image.open(IMAGE_NAME)
pix = im.load()
pos_x = [(i * (im.size[0] - 1)) / (SQRT_NUM_PIXELS - 1) for i in range(SQRT_NUM_PIXELS)]
pos_y = [(i * (im.size[1] - 1)) / (SQRT_NUM_PIXELS - 1) for i in range(SQRT_NUM_PIXELS)]
positions = list(itertools.product(pos_x, pos_y))

pixels = [pix[pos[0], pos[1]] for pos in positions]


# Encrypt all the random pixels
encrypted_pixels = [encrypt(pixel, key) for pixel in pixels]

# Get the exponential inverse of our key
inv = slow_exp_inverse((256**3) + 1, key)

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
        rectCoords = (WIN_OFFSET + i * (IMAGE_WIDTH + WIN_OFFSET) + (y * RECT_WIDTH), 
                      WIN_OFFSET + (x * RECT_HEIGHT),
                      RECT_WIDTH,
                      RECT_HEIGHT)

        # Update our image coordinates correctly
        x = x + 1
        #if(x % SQRT_NUM_PIXELS == 0):
        if(x % SQRT_NUM_PIXELS == 0):
            x = 0
            y = y + 1
            
        
        if (i == 0):
            # We are drawing our original image
            pygame.draw.rect(screen, pixels[j], rectCoords, 0)
        elif (i == 1):
            # We are drawing our encypted image
            pygame.draw.rect(screen, encrypted_pixels[j], rectCoords, 0)
        elif (i == 2):
            # We are drawing our decrypted image
            #pygame.draw.rect(screen, decrypt_exp(encrypted_pixels[j], key), rectCoords, 0)
            pygame.draw.rect(screen, decrypt_exp_2(encrypted_pixels[j], key, inv), rectCoords, 0)

            # Update for sanity
            #if(x % SQRT_NUM_PIXELS == 0):
            #    print str(y * SQRT_NUM_PIXELS + x) + " pixels decrypted"

    # Update the display once all pixel values in the image have been determined
    pygame.display.update()

# Continue to pass indefinitely so that pygame does not exit
while(True):
    pass
