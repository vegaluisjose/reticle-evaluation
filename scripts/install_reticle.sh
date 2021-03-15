#!/bin/bash

set -e
set -u

if [ -d "reticle" ]; then
  rm -rf reticle
fi

# install reticle
git clone https://github.com/vegaluisjose/reticle.git
cd reticle
git checkout tags/pldi2021 -b artifact
cargo build --release
cargo install --bin reticle-translate --bin reticle-optimize --bin reticle-place --path .
cd ..
