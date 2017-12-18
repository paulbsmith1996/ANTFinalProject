# Java 9 on Alpine Linux
FROM openjdk:9-slim
# copies MPC directory into container
COPY . /
WORKDIR /
# creates Java Keystore and Truststore
RUN ./setup-ssl.sh
# launches player in MPC
CMD ./run.sh
