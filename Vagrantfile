Vagrant.configure(2) do |config|
	config.vm.box = "centos7-ansible"
	config.vm.network "private_network", ip: "10.10.10.10"
	config.vm.provision :shell, path: "bootstrap.sh"
end
