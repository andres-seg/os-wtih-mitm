Vagrant.configure("2") do |config|
  # Usar la box local creada
  config.vm.box = "android-x86-test"
  config.vm.box_url = "file://#{File.expand_path('android-x86-rooted.box')}"
  # config.vm.communicator = :none  # para evitar usar SSH
  config.vm.synced_folder "./shared", "/mnt/shared"

  # config.vm.network "public_network"
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 5555, host: 5555, id: "adb", auto_correct: true
  config.ssh.insert_key = false

  # Nombre de la VM en VirtualBox
  config.vm.provider "virtualbox" do |vb|
    vb.name = "android-x86-test"
    vb.memory = 3072
    vb.cpus = 4

    # Configuraciones de video y clipboard
    vb.customize ["modifyvm", :id, "--graphicscontroller", "vboxvga"]
    vb.customize ["modifyvm", :id, "--vram", "96"]
    vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
    vb.customize ["modifyvm", :id, "--draganddrop", "bidirectional"]

    # NOTE: esto es necesario si se quiere montar un ISO (no necesario si se usa una box preconfigurada)
    # vb.customize ["storageattach", :id, "--storagectl", "IDE Controller", "--port", 1, "--device", 0, "--type", "dvddrive", "--medium", "android-x86_64-9.0-r2.iso"]

    # NOTE: una vez que el sistema esté instalado, se debe forzar el arranque desde el disco duro
    # así no se vuelve a mostrar el menú de instalación
    vb.customize ["modifyvm", :id, "--boot1", "disk"]
    vb.customize ["modifyvm", :id, "--boot2", "dvd"]
  end
end
