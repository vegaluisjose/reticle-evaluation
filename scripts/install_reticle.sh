#!/bin/bash

set -e
set -u

if [ -d "reticle" ]; then
  rm -rf reticle
fi

# install z3-solver
pip3 install --user z3-solver

# install reticle
git clone https://github.com/vegaluisjose/reticle.git
cd reticle
# add tag
# git checkout $REV -b artifact 
cargo build --release
cargo install --bin reticle-translate --bin reticle-optimize --bin reticle-place --path .
cd ..
