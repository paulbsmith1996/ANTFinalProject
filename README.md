<<<<<<< HEAD
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
=======
**Before you start, be aware that the current FairplayMP requires multiple physical/virtual machines to run it.**

Reference: [[Readme](http://www.cs.huji.ac.il/project/Fairplay/FairplayMP/Readme.txt)]

Prerequisite
===

``ant 1.8``, ``java``

FairplayMP instructions 
===

Stage 1 - SFDL program:
---

1. Write your program in SFDL2.0 language, you can use the SFLD2.0 specification and examples in the project web site. (You can see the SecondPriceAuction.sfdl example in the package).
2. From inside the compiler directory, compile your program using the command:

```bash
cp sfdl/SecondPriceAuction.sfdl compiler_v1_built/SecondPriceAuction-tocompile.sfdl
cd compiler_v1_built/compiler
java lab.Runner -f ../SecondPriceAuction-tocompile.sfdl
cd ..
ruby Convertor.rb SecondPriceAuction-tocompile.sfdl
# generating files with .cnv, .Opt.circuit , .Opt.fmt
mv *.cnv ..
mv *.Opt.circuit ..
mv *.Opt.fmt ..
```

OR

```bash
java  -cp compiler_v2_built/ sfdl.Compiler sfdl/SecondPriceAuction.sfdl 
```

(Compiler source code is not provided)

Stage 2 - Running the secure multiparty computation:
---

1. Create the ``config.xml`` file fit to the SFDL program. (You can use the ``config.xml`` example in the package - just replace the ip addresses).

2. Deploy the package to each participating computer and run:

```bash
java -cp runtime/build/classes FairplayMP <randomSeed>
```
>>>>>>> FairplayMP/master
