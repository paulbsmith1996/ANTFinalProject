#!/bin/bash

java -cp runtime/build/classes FairplayMP $(openssl rand -base64 18) -v

echo Done!
