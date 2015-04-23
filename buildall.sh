#!/bin/bash
echo "====== Bootstrapping, building and packaging all OS packages ======"
./build-env/bin/fab bootstrap:ct7_64 config_openresty prereqs_openresty build_openresty package_openresty build_clean &
./build-env/bin/fab bootstrap:sl65_64 config_openresty prereqs_openresty build_openresty package_openresty build_clean &
wait

#./build-env/bin/fab bootstrap:sl65_64 config_openresty prereqs_openresty build_openresty package_openresty build_clean
echo "#=================================================================#"
echo "#                                                                 #"
echo "#          CHECK build-output for exported OS packages!           #"
echo "#                                                                 #"
echo "#=================================================================#"
