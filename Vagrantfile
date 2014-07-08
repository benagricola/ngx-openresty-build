# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|

  config.vm.define :sl65_64 do |sl65_64|
    sl65_64.vm.box     = 'centos65-20140113'
    sl65_64.vm.box_url = 'https://dl.dropboxusercontent.com/sh/vxaf1dbg3gtprg0/TJstLu0opb/centos65-kernel3-20140113.box' 
    sl65_64.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512", "--cpus", "2"]
    end
  end
  config.vm.define :trusty_64 do |trusty_64|
    trusty_64.vm.box = "trusty_64"
    trusty_64.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
    trusty_64.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512", "--cpus", "2"]
    end
  end
end
