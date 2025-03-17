Vagrant.configure("2") do |config|

  config.vm.box = 'ubuntu/jammy'

  config.ssh.insert_key = false

  config.vm.synced_folder ".", "/vagrant", disabled: true

  config.vm.provider :virtualbox do |v|
    v.memory = 1800
    v.linked_clone = true
  end


  config.vm.define "app1" do |app|
    app.vm.hostname = "app1.test"
    app.vm.network :private_network, ip: "192.168.56.2"
  end
  config.vm.define "app2" do |app|
    app.vm.hostname = "app2.test"
    app.vm.network :private_network, ip: "192.168.56.3"
  end
  config.vm.define "app3" do |app|
    app.vm.hostname = "app3.test"
    app.vm.network :private_network, ip: "192.168.56.4"
  end
end
