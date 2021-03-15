#!/bin/bash

set -e
set -u

CURRENT_DIR=$( pwd )

# -------- system dependencies
sudo apt-get update
sudo apt-get install xubuntu-core
sudo apt-get install xauth libxrender1 libxtst6 libxi6 virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11 python3-distutils firefox autoconf git make g++

# -------- user installations
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
rm get-pip.py
source ~/.profile

# python packages
pip3 install --user numpy pandas seaborn matplotlib jupyter jupyterlab z3-solver

# rust and rust packages
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env

# -------- user provisioning

mkdir -p ~/Desktop
cd ~/Desktop

# reticle eval
git clone https://github.com/vegaluisjose/reticle-evaluation.git

# install reticle
git clone https://github.com/vegaluisjose/reticle.git
cd reticle
git checkout tags/pldi2021 -b artifact
cargo build --release
cargo install --bin reticle-translate --bin reticle-optimize --bin reticle-place --path .
cd ..

cd $CURRENT_DIR

# Xilinx setup
if [ ! -f Xilinx_profile ]; then
    echo "*****WARNING: Could not find Xilinx_profile! Please configure the paths."
else
    cat Xilinx_profile >> ~/.profile
    cat Xilinx_profile >> ~/.bashrc    
fi

# Make sure we have the right installer and put it in the right place
if [ ! -f Xilinx_Unified_2020.1_0602_1208_Lin64.bin ]; then
    echo "*****WARNING: Xilinx installer not found!"
else
    [ ! -f ~/Xilinx_Unified_2020.1_0602_1208_Lin64.bin ]; then
        cp Xilinx_Unified_2020.1_0602_1208_Lin64.bin ~
    fi
    chmod +x ~/Xilinx_Unified_2020.1_0602_1208_Lin64.bin
fi

# Make a clickable launcher on the desktop
if [ ! Xilinx_installer.desktop ]; then
    echo "*****WARNING: Xilinx installer launcher not found!"
else
    cp Xilinx_installer.desktop ~/Desktop/
fi

echo "SETUP COMPLETED SUCCESSFULLY"

