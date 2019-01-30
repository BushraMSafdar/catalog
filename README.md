﻿﻿﻿﻿﻿﻿# Catalog Application### System Requirements:**Installing vagrant VM:**You will need a virtual machine to run a web server and this web app which uses it. The VM is a Linux system that runs on the top of your machine and hence you can easily share files between your computer and the VM. You will be using the vagrant software to configure and manage the VM.The tools required are:-  **Git**:Download [Git](https://git-scm.com/) and install the version for your operating system. On Wndows, git will provide you with the unix style terminal. For Mac or Linux OS you can use the regular terminal program.- **VirtualBox**:VirtualBox is the actual software that runs the VM. You can download [VirtualBox](https://www.virtualbox.org/) from here. Install the platform package for your operating system. You do not need to the extension pack or sdk and you do not need to launch it.##### Ubuntu 14.04 note: If you are running ubuntu 14.04, install the virtualbox using the ubuntu software center not the virtualbox.org website.- **Vagrant**:Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's file system. Download [Vagrant](https://www.vagrantup.com/) and install the version for your operating system.**Vagrant Configuration File**Open the directory in which vagrant folder is located make an empty folder called catalog in it. Download all the files in it. There will be a file called VagrantFile. Move this file out from this folder into the vagrant folder. This Configuration file is necessary to run the vagrant machine properly.**Running the Virtual machine:**If you are using Windows run the Git bash terminal or if you are using the Mac or Linux system you can use either Git bash or your regular terminal. cd into the directory containing the vagrant folder and then type **vagrant up** to launch your virtual machine.Once its up and running type **vagrant ssh**. This will log your terminal into the virtual machine and you will get a Linux shell prompt. Then type **cd  /vagrant/catalog** to access all the project file.(**Note** make sure that the catalog directory contains all the files i.e. database_setup.py, lotsofitems.py, application.py and two folders named static and templates. you can do that by typing **ls** once you are in the catalog directory.)**Running The Catalog Application:** Now type **python database_setup.py** to initialize the database.Then type **python lotsofitems.py** to populate the database with sports catalog items. If it runs successfully it will print added catalog items! on the git bash terminal. Then type **python application.py** to run the catalog application. Once its running, on your browser visit http://localhost:8000 to view the catalog application. Once you visit this app you will be able to login via your google plus or facebook id. After logging in you will able to create new items and update/delete them.  You can view the items created by yourself or the other users. But you will only be able to update or delete the items you created.