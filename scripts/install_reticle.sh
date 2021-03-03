#!/bin/bash

set -e
set -u

git clone https://github.com/vegaluisjose/reticle.git
cd reticle
# add tag
# git checkout $REV -b artifact 
cargo build --release
cargo install --bin reticle-translate --bin reticle-optimize --bin reticle-place --path .
cd ..
