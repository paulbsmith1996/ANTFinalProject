from server import Server
from client import Client
import os
from rgb_encrypter_jumble_2 import Encrypter

CLIENT_DIR = "client_images/"

print "\nStarting Client"

c = Client()

print "Starting Server"
s = Server()

print "\nClient hashing images"
client_file_names = os.listdir(CLIENT_DIR)
client_hashes_and_ids = []
i = 0
for file_name in client_file_names:
    client_hashes_and_ids.append((c.hash_image(CLIENT_DIR + file_name), i))
    print "Hashed image " + str(i)
    i = i + 1

print "\nServer checking client hashes"
for (hash, id) in client_hashes_and_ids:
    if s.check_legal(hash):
        print "Image " + str(id) + " is legal"
    else:
        print "Image " + str(id) + " is illegal"

print ""
