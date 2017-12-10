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

# Same function as decrypt_exp but quicker, as we take the inverse as input,
# rather than computing it every time we decrypt a pixel
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


# Takes a list (which must be a permutation of [n]) and returns a permutation
# matrix with the rows permuted accordingly
def list_to_matrix(list):

    list_len = len(list)
    mat = np.zeros([list_len, list_len])

    for j in range(list_len):
        mat[j, list[j]] =  1

    return mat

# Takes a matrix representation of a permutation matrix, and generates a list
# of the indices of the non-zero value in each row.
def matrix_to_list(mat):

    list = []

    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if(mat[i, j] != 0):
                list.append(j)
                break

    return list



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


# Returns True if num is prime, and False otherwise
def is_prime(num):

    if num is 1:
        return False

    for i in range(2, int(num ** 0.5) + 1):
        if (num % i == 0):
            return False

    return True


# Generates all primes less than num. This is a naive algorithm.
def gen_primes(num):
    
    primes = []

    for i in range(num):
        if is_prime(i):
            primes.append(i)

    return primes
        





##-------------------------- IMAGE ENCRYPTION FUNCTIONS ---------------------------##

# Encrypts each pixel in the passed pixel list, using the given key
def encrypt_image(pixels, key):

    pix_copy = []
    for pix in pixels:
        pix_copy.append((int(pix[0]), int(pix[1]), int(pix[2])))

    return [encrypt(pixel, key) for pixel in pix_copy]

# Decrypts each pixel in the passed pixel list, using the given key
def decrypt_image(encrypted_pixels, key):
    inv = slow_exp_inverse((256**3) + 1, key)

    enc_pix = []
    for pix in encrypted_pixels:
        enc_pix.append((int(pix[0]), int(pix[1]), int(pix[2])))

    return [decrypt_exp_2(pixel, key, inv) for pixel in enc_pix]

# Jumbles the pixels in the passed pixel list, using the 2 permutation matrices,
# P and Q. P permutes the rows of the pixel list and Q permutes the pixel list's
# columns.
def jumble_image(pixels, P, Q):
    P_1 = P
    P_2 = Q

    # P_1 and P_2 should be width x width and height x height matrices respectively
    # for our image permutation to be a valid operation.
    width = P_1.shape[0]
    height = P_2.shape[0]

    # Need to make a deep copy (due to a bug fix), otherwise numpy handles the
    # matrix multiplication bizarrely.
    unjum_pix = []
    for pix in pixels:
        unjum_pix.append((int(pix[0]), int(pix[1]), int(pix[2])))

    # Get the corresponding indices of the pixels in our list
    indices = [rgb_to_index(pixel) for pixel in unjum_pix]
    inds = np.asarray(indices)

    # Reshape our list in order to perform the matrix multiplications
    square_inds = inds.reshape([width, height])
    square_inds = P_1.dot(square_inds).dot(P_2)

    # Transform resulting matrix back into a list
    jumbled_inds = square_inds.reshape([width * height, 1])
    return [index_to_rgb(index) for index in jumbled_inds]


# Reverses the jumble operation on an image. P_1 and P_2 represent the matrices
# used to originally jumble the pixels.
def unjumble_image(jumbled_pixels, P_1, P_2):
    
    # P_1 and P_2 should be width x width and height x height matrices respectively
    # for our image permutation to be a valid operation.
    width = P_1.shape[0]
    height = P_2.shape[0]

    # Need to make a deep copy (due to a bug fix), otherwise numpy handles the
    # matrix multiplication bizarrely.
    jum_pix = []
    for pix in jumbled_pixels:
        jum_pix.append((int(pix[0]), int(pix[1]), int(pix[2])))

    # Get the corresponding indices of the pixels in our list
    indices = [rgb_to_index(pixel) for pixel in jum_pix]
    inds = np.asarray(indices)

    # Reshape our list in order to perform the matrix multiplications
    square_inds = inds.reshape([width, height])

    # The transpose of a permutation matrix is its inverse
    square_inds = (P_1.T).dot(square_inds).dot(P_2.T)

    jumbled_inds = square_inds.reshape([width * height, 1])
    return [index_to_rgb(index) for index in jumbled_inds]
    
    



##--------------------------- EXECUTABLE CODE ------------------------##


class Encrypter:

    # Define a number of constants for file name simplification/standardization
    PNG_EXT = ".png"
    JPG_EXT = ".jpg"
    TXT_EXT = ".txt"
    
    ENCRYPT_TAG = "_encrypted"
    KEY_TAG = "_key"
    MATRIX_TAG = "_matrix"
    
    # Set constants for graphics in pygame
    WIN_OFFSET = 10
    
    IMAGE_WIDTH = 450
    IMAGE_HEIGHT = 500
    
    WINDOW_WIDTH = (3 * IMAGE_WIDTH) + (4 * WIN_OFFSET)
    WINDOW_HEIGHT = IMAGE_HEIGHT + 2 * WIN_OFFSET

    # Determine the number of pixels in our desired image
    NUM_PIXELS = 400 * 600
    SQRT_NUM_PIXELS = int(NUM_PIXELS ** 0.5)

    # Encrypts plain text image, then displays the plain text, encrypted, and decrypted images
    # all side-by-side
    def __init__(self, image_name):
        if(image_name is None):
            print "Please indicate a file to encrypt"
            return

        self.image_name = image_name

    def run(self):

        print "Encrypter started"
        self.im_width  = 0
        self.im_height = 0

        self.rect_width = 1
        self.rect_height = 1

        # Get the pixel information from the image with file name "image_name"
        self.pixels = self.get_image()

        # Generate random key and matrices for encryption
        self.key, self.P_1, self.P_2 = self.load_crypto()

        # Encrypt image with our scheme
        self.encrypted_pic = self.gen_encrypted_image(self.pixels, self.key, self.P_1, self.P_2)

        # Decrypt image to assure user of correct working
        self.decrypted_pic = self.gen_decrypted_image(self.encrypted_pic, self.key, self.P_1, self.P_2)

        # Display the results of encryption and decryption using pygame
        self.display_results(self.pixels, self.encrypted_pic, self.decrypted_pic)

    # Generates a random key using a randomized algorithm, this should work better in expectation
    # than simply generating all primes less than (256 **3), and choosing one at random.
    def gen_rand_key(self):
        key = 6
        while not is_prime(key):
            key = np.random.randint(2, (256 ** 3))
        return key
        

    # Get the pixel information in the file with name "image_name"
    def get_image(self):

        print "\nGetting image"

        # Get the pixels of a given image and find the pixels we are interested in
        im = Image.open(self.image_name + Encrypter.JPG_EXT)
        pix = im.load()

        hw_ratio = float(im.size[1]) / float(im.size[0])

        self.im_width = int((float(Encrypter.NUM_PIXELS) / hw_ratio) ** 0.5)
        self.im_height = Encrypter.NUM_PIXELS / self.im_width

        #self.rect_width = int(float(Encrypter.IMAGE_WIDTH) / float(self.im_width))
        #self.rect_height = int(float(Encrypter.IMAGE_HEIGHT) / float(self.im_height))

        # We are only finding a small subset of pixels (in this version). This significantly speeds up encryption
        # process and significantly decreases resolution.
        pos_x = [(i * (im.size[0] - 1)) / (self.im_width - 1) for i in range(self.im_width)]
        pos_y = [(i * (im.size[1] - 1)) / (self.im_height - 1) for i in range(self.im_height)]
        positions = list(itertools.product(pos_y, pos_x))
        
        return [pix[pos[1], pos[0]] for pos in positions]
        

    # Get a random key and permutation matrices to encrypt the image
    def load_crypto(self):

        # Generate key in Z_{256 ** 3}
        key = self.gen_rand_key()

        # Generate 2 permutation matrices, whose sizes are determined by the 
        # NUM_PIXELS parameter.
        P_1_list = np.random.permutation(range(self.im_width))
        P_2_list = np.random.permutation(range(self.im_height))

        P_1 = list_to_matrix(P_1_list)
        P_2 = list_to_matrix(P_2_list)

        # Save key to an appropriately named file
        print "Saving key"
        key_file = open(self.image_name + Encrypter.KEY_TAG + Encrypter.TXT_EXT, "w+")
        key_file.write(str(key))
        key_file.close()

        # Save permutation matrices to an appropriately named file
        print "Saving permutation matrices"        
        mat_file = open(self.image_name + Encrypter.MATRIX_TAG + Encrypter.TXT_EXT, "w+")
        mat_file.write(str(P_1_list))
        mat_file.write(str(P_2_list))
        mat_file.close()

        return (key, P_1, P_2)


    # Encrypt the image reprsented by the passed pixel list, using the random key
    # and permutation matrices generated by load_crypto() function
    def gen_encrypted_image(self, pixels, key, P_1, P_2):
        
        # Encrypt pixels one-by-one
        print "Encrypting pixels"
        encrypted_pixels = encrypt_image(pixels, key)

        # Jumbled encrypted pixels
        print "Jumbling image"
        jumbled_pixels = jumble_image(encrypted_pixels, P_1, P_2)

        # Save encrypted image to appropriately named file
        print "Saving encrypted Image"
        jum_pix = np.asarray(jumbled_pixels).reshape([self.im_width, self.im_height, 3])
        im = Image.fromarray(jum_pix.astype('uint8'))
        im.save(self.image_name + "_encrypted" + Encrypter.PNG_EXT)

        return jumbled_pixels


    # Decrypt the image represented by the pixel list, using the saved key and permutation matrices
    def gen_decrypted_image(self, pixels, key, P_1, P_2):

        # Unjumble pixels
        print "Unjumbling jumbled image"
        unjumbled_pixels = unjumble_image(pixels, P_1, P_2)
        
        # Decrypt the jumbled pixels one-by-one
        print "Decrypting pixels"
        decrypted_pixels = decrypt_image(unjumbled_pixels, key)

        return decrypted_pixels


    # Use pygame to draw the plain text, encrypted, and decrypted images
    def display_results(self, plain_pix, encrypted_pix, decrypted_pix):

        print "Initializing pygame\n"

        # Boot up a pygame window and adjust size
        pygame.init()
        screen = pygame.display.set_mode((Encrypter.WINDOW_WIDTH, Encrypter.WINDOW_HEIGHT))

        print "\nDrawing images"

        # Produce our 3 images: the image on the left will be our "plaintext" image.
        # In the center we have the encrypted image, and on the right we have the 
        # decrypted image
        for i in range(3):
    
            # Keep track of our x and y coordiantes within the image we are displaying
            x = 0
            y = 0

            # Loop through all pixels in our images
            for j in range(len(plain_pix)):

                # Set the x, y, width, and length of the current pixel we are drawing
                rectCoords = (Encrypter.WIN_OFFSET + i * (Encrypter.IMAGE_WIDTH + Encrypter.WIN_OFFSET) + (x * self.rect_width), 
                              Encrypter.WIN_OFFSET + (y * self.rect_height),
                              self.rect_width,
                              self.rect_height)

                # Update our image coordinates correctly
                x = x + 1
                # if(x % SQRT_NUM_PIXELS == 0):
                if(x % self.im_width == 0):
                    x = 0
                    y = y + 1
            
        
                if (i == 0):
                    # We are drawing our original image
                    pygame.draw.rect(screen, plain_pix[j], rectCoords, 0)
                elif (i == 1):
                    # We are drawing our encrypted image
                    pygame.draw.rect(screen, encrypted_pix[j], rectCoords, 0)
                elif (i == 2):
                    # We are drawing our decrypted image
                    pygame.draw.rect(screen, decrypted_pix[j], rectCoords, 0)

                    # Update for sanity
                    # if(x % SQRT_NUM_PIXELS == 0 and y % 20 == 0):
                    #    print str(y * SQRT_NUM_PIXELS) + " pixels decrypted"

            # Update the display once all pixel values in the image have been determined
            pygame.display.update()

        print "Images drawn\n"

        # Continue to pass indefinitely so that pygame does not exit
        sleep(10)
        print "Exiting\n"


# Create a new Encrypter that encrypts the image in the file with the passed name
#if len(sys.argv) > 1:
#    e = Encrypter(sys.argv[1])
#    e.run()
#else:
    # Program fails nicely on this Encrypter
#    e = Encrypter(None)
