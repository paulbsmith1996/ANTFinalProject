#!/bin/bash

java -cp runtime/build/classes FairplayMP $(openssl rand -base64 6) -v

echo Done!
