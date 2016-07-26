# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|

  config.vm.define :ct7_64 do |ct7_64|
    ct7_64.vm.box = "http://cloud.centos.org/centos/7/vagrant/x86_64/images/CentOS-7-x86_64-Vagrant-1602_02.VirtualBox.box"
    ct7_64.vm.box_download_checksum = "8dc6c0a4e93af0de9da7ac4b91d3a2710ff9ff58ce2792ecf4c73542a22421b4"
    ct7_64.vm.box_download_checksum_type = "sha256"
    ct7_64.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512", "--cpus", "5"]
      vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
      vb.customize ["modifyvm", :id, "--hpet", "on"]
    end
  end
  config.vm.define :sl65_64 do |sl65_64|
    sl65_64.vm.box     = 'centos66-tommy'
    sl65_64.vm.box_url = 'https://github.com/tommy-muehle/puppet-vagrant-boxes/releases/download/1.0.0/centos-6.6-x86_64.box' 
    sl65_64.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512", "--cpus", "5"]
      vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
      vb.customize ["modifyvm", :id, "--hpet", "on"]
    end
  end
  config.vm.define :trusty_64 do |trusty_64|
    trusty_64.vm.box = "trusty_64"
    trusty_64.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
    trusty_64.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512", "--cpus", "2"]
      vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
      vb.customize ["modifyvm", :id, "--hpet", "on"]
    end
  end
end
