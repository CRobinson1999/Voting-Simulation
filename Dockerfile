# For now, can only use py2wasm with 3.11
ARG COMPILER=python:3.11-bookworm
ARG HOST=nginx:1.27-bookworm
FROM $COMPILER AS builder

RUN pip install py2wasm
RUN apt update && apt install patchelf

ADD voting-simulation /root/voting-simulation
WORKDIR /root/voting-simulation

RUN py2wasm Voting-M1.py -o voting-simulation.wasm

FROM $HOST

COPY --from=builder /root/voting-simulation/voting-simulation.wasm /usr/share/nginx/html/voting-simulation.wasm
ADD index.html /usr/share/nginx/html/index.html
#ADD nginx.conf /etc/nginx/nginx.conf
