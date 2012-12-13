# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.define :precise_64 do |precise_64|
    precise_64.vm.box = "precise_64"
    precise_64.vm.box_url = "http://files.vagrantup.com/precise64.box"
    precise_64.vm.customize ["modifyvm", :id, "--memory", 512]
  end
  config.vm.define :precise_32 do |precise_32|
    precise_32.vm.box = "precise_32"
    precise_32.vm.box_url = "http://lawlr.us/precise32.box"
    precise_32.vm.customize ["modifyvm", :id, "--memory", 512]
  end
  config.vm.define :sl63_64 do |sl63_64|
    sl63_64.vm.box = "sl63_64"
    sl63_64.vm.box_url = "http://lyte.id.au/vagrant/sl6-64-lyte.box"
    sl63_64.vm.customize ["modifyvm", :id, "--memory", 512]
  end
end
