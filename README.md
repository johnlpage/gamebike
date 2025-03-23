# Exercise Equipment game controller (Bike)

# About 

# Requirements

* Rasbian Bullseye (Bookworm had issues) Lite
* Xoss Cycing speed sensot
* Arduino Nanao 33 BLE (Steering Sensor)
* WAHOO KICKR TRAINER (Work in Progress)


# Install

```
 sudo apt update
 sudo apt upgrade
 sudo yum install -y git
 git clone git@github.com:johnlpage/gamebike.git

 cd gamebike
 # Runnign in Venv isn't working for me
 #sudo  apt-get install python3-venv
 #source bin/activate
 ##python3 -m venv .

sudo apt install -y python3-pip
sudo pip install  -r requirements.txt 



```