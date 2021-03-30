#!/bin/bash

#### Set up python

sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2

sudo apt install python3-pip

sudo apt-get update

sudo apt install git

git clone https://github.com/uayebforever/dotfiles.git .dotfiles

cd dotfiles || exit 1

git clone https://github.com/ohmyzsh/ohmyzsh.git oh-my-zsh

source .dotfiles/zsh/setup.sh

# Install JPEG2000 support required for Pillow
sudo apt install libopenjp2-tools libopenjp2-7 libopenjp2-7-dev