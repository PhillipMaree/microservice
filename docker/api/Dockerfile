FROM python:3

ENV DEBIAN_FRONTEND=noninteractive

ARG USER_NAME

ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"

# generic packages
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y  \
    keyboard-configuration \ 
    python3-venv \
    curl \
    sudo 

# install python depencies
ADD /include ./microservice
RUN pip install --upgrade pip --no-cache-dir -r ./microservice/requirements.txt

# create user working directory
RUN useradd -d /home/${USER_NAME} -m ${USER_NAME} && \
    chown -R ${USER_NAME} /home/${USER_NAME} && \
    adduser ${USER_NAME} sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER $USER_NAME
ENV HOME /home/$USER_NAME
ARG workdir=/home/$USER_NAME
WORKDIR $workdir

CMD [ "python", "backend.py" ]