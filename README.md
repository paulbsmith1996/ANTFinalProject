# Image Encryption

Prerequisites (we recommend using a virtual environment):
``$ pip install -r requirements.txt``

This program implements an interesting but likely unsound and expensive
cryptographic scheme for images. The goal here is to produce make our
image data readable at every level or our encryption protocol: the plain
image should obviously be readable, as should the decrypted image, but
we go a step further and make the encrypted image readable as well.

This is obviously not recommended for an efficient cryptographic system,
where we would want to utilize standard image encryption algorithms to
minimize our memory usage and time complexity. Our goal is more
mathematical an artistic than anything else.

Therefore, we need to develop an encryption scheme that encodes each
pixel's as a readable RGB tuple. We do this by assigning each possible
pixel value to a number in Z_{(256^3)} (we essentially write the pixel's
RGB value as a number base 256). This is a unique encoding for each
possible pixel value. We then work in the group Z_{(256^3 + 1)}* , the
units of the group.

Translation from an "index" to an "RGB" value is implemented below, as
is the reverse operation.

We also do not claim that our scheme is secure, as this number is easily
factorized and this factorization can then be used to break our system
quickly, though this is not necessarily obvious for large images.

# Secure Multi-Party Computation

Prerequisites: ``ant 1.8``, ``java``, ``ruby``

This program complements our Image Encryption above. Instead of using a hash function invariant for both the encrypted and the unencrypted versions of an image, we implement a Multi-Party computation "game" between 3 parties: a client (e.g. end-user), a server (e.g. Dropbox) and at least one image-provider (e.g. government agency). For each player, their input is kept secret from the other players and the output is a single bit: whether the provided image is illegal or not.

Because of restrictions by the Fairplay language (see reference below), an image is represented as a number. Each player must provide exactly one image for the computation to work.

Run as follows:
* Modify constants in ``sfdl/IllegalImages.sfdl`` to the desired number of players and illegal image threshold
* ``$ ./build.sh``
* Modify players' IP addresses in ``config.xml``
* ``$ docker build -t my-java-app .``
* ``$ docker run -i -t my-java-app``

The last command must by run in attached mode, in as many terminal windows as there are players in your SFDL program.

**Use Docker on a Linux (Ubuntu 16.04) to avoid networking issues. On macOS, containers cannot communicate via their IP addresses.**

Reference: [[FairplayMP Paper](http://www.cs.huji.ac.il/project/Fairplay/FairplayMP/)]
