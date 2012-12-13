#!/bin/bash
echo "====== Bootstrapping, building and packaging all OS packages ======\n"
./build-env/bin/fab bootstrap:sl63_64,precise_32,precise_64 config_openresty prereqs_openresty build_openresty package_openresty build_clean
echo "#=================================================================#\n"
echo "#                                                                 #\n"
echo "#          CHECK build-output for exported OS packages!           #\n"
echo "#                                                                 #\n"
echo "#=================================================================#\n"