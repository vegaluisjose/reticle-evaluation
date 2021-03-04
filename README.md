# Reticle Evaluation

This repository contains the evaluation materials for our PLDI 2021 paper, "Reticle: A Virtual Machine for Programming Modern FPGAs".

## Getting Started Guide

### Virtual Machine (VM) setup

The VM is packaged as an OVA file and can be downloaded from a permanent link here.
Our instructions assume you're using [VirtualBox](https://www.virtualbox.org).

- Minimum host disk space required to install external tools: 65 GB
- Increase number of cores and RAM
  - Select the VM and click "Settings".
  - Select "System" > "Motherboard" and increase the "Base Memory" to 8 GB.
  - Select "System" > "Processor" and select at least 2 cores.

<details>
<summary><b>Troubleshooting common VM problems</b> [click to expand]</summary>

 - **Running out of disk space while installing Vivado tools**. The Vivado installer will sometimes
 crash or not start if there is not enough disk space. The Virtual Machine is configured to use
 a dynamically sized disk, so to solve this problem, simply clear space on the host machine. You need about 65 gbs of free space.
 - **Running out of memory**. Vivado uses fair amount of memory. If there
 is not enough memory available to the VM, they will crash and data won't be generated. If something fails you can do one of:
   - Increase the RAM and rerun the script that had a failure.
   - Ignore the failure, the figure generation scripts are made to be resilient to this kind of data failure.
 - **Kernel driver not installed (rc=-1908)**. Proper virtualbox permissions have to be setup for OSx, read more [here](https://www.howtogeek.com/658047/how-to-fix-virtualboxs-“kernel-driver-not-installed-rc-1908-error/)
</details>

### Installing Xilinx Vivado (Estimated time: 2-4 hours)
Our evaluation uses Xilinx's Vivado tools to generate
area and resource estimates.
Unfortunately due to licensing restrictions, we can't distribute the VM with
these tools installed. However, the tools are freely available and below are
instructions on how to install them.

Our evaluation requires **Vivado WebPACK v.2020.1**.
Due to the instability of synthesis tools, we cannot guarantee our
evaluation works with a newer or older version of the Vivado tools.

If you're installing the tools on your own machine instead the VM, you can
[download the installer](https://www.xilinx.com/member/forms/download/xef.html?filename=Xilinx_Unified_2020.1_0602_1208_Lin64.bin).


The following instructions assume you're using the VM:

1. Log in to the VM with the username `reticle` and the password `reticle`.
2. The desktop should have a file named: `Xilinx Installer`. Double click on this to launch the installer.
3. Ignore the warning and press `Launch Anyway`.
4. When the box pops up asking you for a new version, click `Continue`.
5. Enter your Xilinx credentials. If you don't have them, [create a Xilinx account](https://login.xilinx.com/login/login.htm).
  - **Note** When you create an account, you need to fill out all the required information on your profile.
  Otherwise the Xilinx installer will reject your login.
  - The "User ID" is the email address of the Xilinx account you created.
6. Agree to the contract and press `Next`.
7. Choose `Vivado` and click `Next`.
8. Choose `Vivado HL WebPACK` and click `Next`.
9. Leave the defaults for selecting devices and click `Next`.
10. **Important!** Change the install path from `/tools/Xilinx` to `/home/reticle/Xilinx`.
11. Confirm that you want to create the directory.
12. Install.  Depending on the speed of your connection, the whole process
    should take about 2 - 4 hrs.
    
### Building and installing Reticle (2-5 min)

1. Go to `reticle-evaluation` folder, run `cd ~/Desktop/reticle-evaluation`
2. Update repository, run `git pull`
3. Build and install `reticle`, run `bash scripts/install_reticle.sh`

### Test Reticle installation

## Step-by-Step Guide

### Data generation

The following commands generate data for plotting Figures 14(a)(b)(c).

* Generate compile run-time data `python3 scripts/compiler_runtime.py`
* Generate program run-time and resource usage data `python3 scripts/program_metrics.py`
