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
is the reverse operation.

We also do not claim that our scheme is secure, as this number is easily
factorized and this factorization can then be used to break our system
quickly, though this is not necessarily obvious for large images.

Dependent on pygame and numpy libraries
