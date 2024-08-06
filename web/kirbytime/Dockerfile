FROM ubuntu:20.04 as chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user
RUN apt update -y
RUN apt install python3-pip -y

COPY main /home/user/main

RUN chown -R user:user /home/user/main/
RUN chmod 744 /home/user/main/

RUN pip3 install -r /home/user/main/requirements.txt

USER user

EXPOSE 8000

CMD echo "HI" && cd /home/user/main && gunicorn --bind 0.0.0.0:8000 main:app
