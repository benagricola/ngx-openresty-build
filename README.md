# Openresty Build

## Intro

The idea of this is to spawn Virtualbox VM's using vagrant, build openresty or whatever (currently just openresty), then clean up and shut down.

## Supports

 * Ubuntu Precise (32 / 64 bit)
 * Scientific Linux 6.3 (64 bit)

## Howto 

Install Virtualbox, Vagrant and Python / pip virtualenv. Check out the Repo, cd into the directory.

    virtualenv build-env
    build-env/bin/pip install -r requirements.txt
    ./buildall.sh

## Notes

It isn't clean, it isn't pretty, it also isn't that fast. But it works, and it's a 1-command build system for the packages I wanted.

## TODO

Make the VM's shut down once finished :)

## Author

Ben Agricola <bagricola@squiz.co.uk>

## Licence

This module is licensed under the 2-clause BSD license.

Copyright (c) 2012, Ben Agricola <bagricola@squiz.co.uk>

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.     
