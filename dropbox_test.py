from PIL import Image
from server import Server
from client import Client
import os
from rgb_encrypter_jumble_2 import Encrypter

CLIENT_DIR = "client_images/"
ILLEGAL_PIC = CLIENT_DIR + "bear.png"

print "\nStarting Client"

c = Client()

print "Starting Server"
s = Server()

print "\nClient hashing images"
client_file_names = os.listdir(CLIENT_DIR)
client_hashes_and_ids = []
i = 0
for file_name in client_file_names:
    if file_name[len(file_name) - 4:] == ".png" and "encrypted" not in file_name:
        client_hashes_and_ids.append((c.hash_image(Image.open(CLIENT_DIR + file_name)), i))
        print "Hashed image " + str(i)
        i = i + 1

print "\nServer checking client hashes"
for (hash, id) in client_hashes_and_ids:
    if s.check_legal(hash):
        print "Hash " + str(id) + " is legal"
    else:
        print "Hash " + str(id) + " is illegal"


print ""
j = 0
for file_name in client_file_names:
    if file_name[len(file_name) - 4:] == ".png" and "encrypted" not in file_name:
        if c.hash_image(Image.open(CLIENT_DIR + file_name)) not in s.illegal_hashes:
            print "Client encrypting image " + str(j)
            c.encrypt_image(CLIENT_DIR + file_name)
            print ""

        j = j + 1

client_file_names = os.listdir(CLIENT_DIR)
print "\nClient uploading images to server"
for file_name in client_file_names:
    if file_name[len(file_name) - 4:] == ".png" and "_encrypted" in file_name:
        c.upload_image(CLIENT_DIR + file_name, s)

print "\nClient attempting to upload illegal picture " + ILLEGAL_PIC
c.encrypt_image(ILLEGAL_PIC)
print ""
c.upload_image(ILLEGAL_PIC[:len(ILLEGAL_PIC) - 4] + "_encrypted.png", s)
        

print "\nClient retrieving images from server"
c.retrieve_images(s)


print ""
