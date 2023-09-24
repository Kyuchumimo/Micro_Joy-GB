# Micro Joy-GB
![micro_joy-gb](https://github.com/Kyuchumimo/Micro_Joy-GB/assets/74131798/a6889ac3-33b7-4171-9563-164dc3a5d953)

This software is divided into 2 parts: master (computer) and slave (microcontroller).  

The master program "mcu_write7.py" requires the following dependencies:  
PyBoy  
Pillow (PIL Fork)  
pySerial  

The slave program "boot.py" requires the following dependencies:  
micropython-pcd8544  
micropython-sn76489  
micropython-74hc595  

To load games, replace "game.gb" by the directory and/or filename to a valid GB ROM.  

## How it works?
![flowchart drawio](https://github.com/Kyuchumimo/Micro_Joy-GB/assets/74131798/58936860-4332-4000-b61c-dc8a89d30b52)
