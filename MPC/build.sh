#!/bin/bash

echo Building File...
cp sfdl/Millionaires.sfdl compiler_v1_built/Millionaires-tocompile.sfdl
cd compiler_v1_built/compiler
java lab.Runner -f ../Millionaires-tocompile.sfdl
cd ..
ruby Convertor.rb Millionaires-tocompile.sfdl

# generating files with .cnv, .Opt.circuit , .Opt.fmt
mv *.cnv ../Millionaires-compiled.sfdl.cnv
mv *.Opt.circuit ../Millionaires-compiled.sfdl.Opt.circuit
mv *.Opt.fmt ../Millionaires-compiled.sfdl.Opt.fmt

echo Done!
