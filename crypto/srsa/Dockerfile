FROM ubuntu:20.04 as chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user
RUN apt update -y
RUN apt install socat -y
RUN apt install python3 -y
RUN apt install python3-pip -y

RUN pip3 install pycryptodome

COPY chal.py /home/user/chal.py
COPY flag.txt /home/user/flag.txt
COPY run.sh /home/user/run.sh

WORKDIR /home/user

USER user

EXPOSE 4242

CMD echo "HI" && socat TCP-LISTEN:4242,reuseaddr,fork EXEC:"/home/user/run.sh"
