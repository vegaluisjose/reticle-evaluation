# Creating the Reticle Artifact  VM

Below is the step-by-step process used for creating the VM for the Reticle artifact evaluation.

It uses VirtualBox to create the VM, and uses SSH to move files onto the VM.

## Prerequisites
Make sure you have VirtualBox installed ([https://www.virtualbox.org/](https://www.virtualbox.org/)).

You will also need the correct version of the [Xilinx Installer](https://www.xilinx.com/member/forms/download/xef.html?filename=Xilinx_Unified_2020.1_0602_1208_Lin64.bin) and a compatible version of Ubuntu, like the
[Ubuntu 18.04.4 ISO](http://old-releases.ubuntu.com/releases/18.04.4/ubuntu-18.04-live-server-amd64.iso).

> **Important: If you don't use the ISO linked above, please pay special attention to the supported Linux versions for the Xilinx tooling: even on older LTS releases, the newer point releases are unsupported. You may have to dig up an older point release to be compatible.**

Make sure you have the script with all the necessary server setup (`setup.sh`).

Lastly, you will need a couple files to streamline the Xilinx installation for the end-user: `Xilinx_installer.desktop` and `Xilinx_profile`.

## Creating the Virtual Machine
### Initial Setup
Launch VirtualBox and click "New" to create a new virtual machine. Use the following settings:
 - **Name** - "reticle-artifact-vm" or some other suitable name (this will be permanent and visible)
 - **Machine Folder** - where to store the VM on the current host machine (irrelevant)
 - **Type** - "Linux"
 - **Version** - "Ubuntu (64-bit)"

### Memory and Disk Allocation
In the next window, set the memory size to 8GB (Vivado can get memory hungry).

After that, select "Create a virtual hard disk now".
Select "VMDK (Virtual Machine Disk)" (this gives the most portability).
Select "Dynamically allocated".
"File location:" leave as default (or put it somewhere else).
"Size:" 100GB (this gives ample space for the Xilinx and software installations).

### Attach the ISO for Installation
Open the settings for the newly-created virtual machine. 
Under "Storage", click on "Controller: IDE" and create a new optical drive. 
Select the Ubuntu ISO you downloaded and click "Choose". 
Then, select the new device (Ubuntu ISO) from the list and make sure "Live CD" is checked under "Attributes".

### Install OS
Launch the VM and go through the steps to install Ubuntu, choosing the default options. Install to the virtual disk we created and select "use entire disk". 

In the profile setup, choose an appropriate name and server name, like "reticle" and "reticle-vm". 
The username should be "reticle" and the password should be "reticle".

When the installation finishes, hit "reboot now."

## Configure the VM

### Fix Version String for Xilinx
Log in to the machine.

To stop the Xilinx installer from mistakenly thinking this is an incompatible version of Ubuntu, open "/etc/os-release" (with sudo) and modify all the version strings from "18.04" to "18.04.4".
E.g., run `sudo nano /etc/os-release` and change the version strings, such that the lines
```
VERSION="18.04 LTS (Bionic Beaver)"
PRETTY_NAME="Ubuntu 18.04 LTS"
VERSION_ID="18.04"
```
all become
```
VERSION="18.04.4 LTS (Bionic Beaver)"
PRETTY_NAME="Ubuntu 18.04.4 LTS"
VERSION_ID="18.04.4"
```

### Install SSH to Access VM
Run `sudo apt-get update` to refresh the package list, then `sudo apt-get install openssh-server` .
After that finishes, shut down the VM.

Open the VM's settings. 
Under "Network" open the "Advanced" section of the adapter and click "Port Forwarding". 
Use the "+" to create a new rule, configured with:
- Name - SSH
- Protocol - TCP
- Host IP - 127.0.0.1
- Host Port - 5051 (any port number works here, just use the same one when you connect)
- Guest IP - (blank)
- Guest Port - 22

>**While you're in the settings, go back under "Storage" and remove the live CD entry.**

Save and exit the settings.

## Install Software

Launch the VM.

From the **host** machine (not the VM), open a terminal in the folder with the setup files and transfer them to the VM. E.g.,
`scp -oPort=5051 setup.sh Xilinx_installer.desktop Xilinx_profile Xilinx_Unified_2020.1_0602_1208_Lin64.bin reticle@127.0.0.1:~`
(If you used a different port number, change that in the command.)

Log into the VM. The files should be waiting for you in the home folder. Run the setup with
`bash setup.sh`
and follow the prompts as necessary (it will stop several times for you to hit "Y" or select the default options).

## Export the VM

When everything has finished, export an image of the VM by shutting down, right clicking it in the list, and selecting "Export to OCI". Export it to an appropriate file (like the default).

> **This file is the image that will be shipped. To test/play with it, import it into VirtualBox and do things there, but do not overwrite the image file with a new export unless you want those changes to be permanent.**

## Testing
To test the VM, import it into VirtualBox, launch it, and then run the commands to check everything (e.g., Xilinx installs correctly, Rust is installed, python and z3 are working, etc.).







