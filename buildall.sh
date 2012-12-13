#!/bin/bash
echo "====== Bootstrapping, building and packaging all OS packages ======"
./build-env/bin/fab bootstrap:sl63_64,precise_32,precise_64 config_openresty prereqs_openresty build_openresty package_openresty build_clean
echo "#=================================================================#"
echo "#                                                                 #"
echo "#          CHECK build-output for exported OS packages!           #"
echo "#                                                                 #"
echo "#=================================================================#"
