#!/bin/bash

echo Building File...
cp sfdl/IllegalImages.sfdl compiler_v1_built/IllegalImages-tocompile.sfdl
cd compiler_v1_built/compiler
java lab.Runner -f ../IllegalImages-tocompile.sfdl
cd ..
ruby Convertor.rb IllegalImages-tocompile.sfdl

# generating files with .cnv, .Opt.circuit , .Opt.fmt
mv *.cnv ../IllegalImages-compiled.sfdl.cnv
mv *.Opt.circuit ../IllegalImages-compiled.sfdl.Opt.circuit
mv *.Opt.fmt ../IllegalImages-compiled.sfdl.Opt.fmt

echo Done!
