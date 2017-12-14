#!/bin/bash

echo Creating Keystore…
keytool -genkeypair -keystore node1.keystore -keyalg RSA -alias node1 -dname "CN=node1.example.com,O=Hadoop" -storepass changeme -keypass changeme -validity 90
echo Keystore created with password: changeme

echo Creating Certificate…
keytool -exportcert -keystore node1.keystore -alias node1 -storepass 123456 -file node1.cer
echo Certificate created

echo Creating Truststore…
keytool -importcert -keystore custom.truststore -alias node1 -storepass trustchangeme -file node1.cer -noprompt
echo Truststore created with password: trustchangeme

echo Moving into certificate/ directory…
mkdir certificate

mv custom.truststore certificate
mv node1.keystore certificate
mv node1.cer certificate
echo Done!
