# Reticle Evaluation

This repository contains the evaluation materials for the PLDI 2021 paper, "Reticle: A Virtual Machine for Programming Modern FPGAs". The repository can be found on [github](https://github.com/vegaluisjose/reticle-evaluation). (If you're reading these instruction in a text file, we recommend visiting the link above to see a markdown-formatted version.)

### Claims
The central claims of the Reticle paper all build on the idea that the traditional synthesis tools are inadequate for compiling designs for modern FPGAs. To improve this situation, we develop a new language IR and compiler to handle FPGA synthesis. Specifically, compared to the synthesis flows of Xilinx Vivado, Reticle:
 -  **Claim A:** Is faster (up to 100x) synthesizing the same design;
 -  **Claim B:** Is more predictable;
 -  **Claim C:** More efficiently exploits DSPs;
 -  **Claim D:** Produces potentially faster designs from better DSP usage;
 -  **Claim E:** Is extensible for new instructions/resources.

These claims are all supported by the artifact. Claims **A - D** are discussed after generating comparison data for the example programs in the "Step-by-Step Guide". Claim **E** is substantiated with the exercise at the end of the "Getting Started" guide (adding a new instruction to the compiler).




## Getting Started Guide

This section will help you set up the virtual machine, install Reticle, and then test out some features of the Reticle system. It should take less than 30 minutes to complete.

### Virtual Machine (VM) Setup

The VM is packaged as an OVA file and can be downloaded from [Google Drive](https://drive.google.com/file/d/1YcpfbMFsuyrwOxiVnV4bZUUdTG8o74XW/view?usp=sharing).
Our instructions assume you're using [VirtualBox](https://www.virtualbox.org).

#### Requirements/Setup (5-10 min)
Download the VM image from [Google Drive](https://drive.google.com/file/d/1YcpfbMFsuyrwOxiVnV4bZUUdTG8o74XW/view?usp=sharing). You can verify its integrity by checking that the MD5 checksum matches `d8dc7563f18e3f030d1ed7e5d146f82c`.

Once downloaded, import the OVA image into VirtualBox with the "Import Appliance" option under the "File" menu.

The minimum host disk space required to install external tools is **65 GB**. Furthermore, to to ensure that the Xilinx tools do not crash from resource exhaustion, we recommend increasing the number of cores and RAM allocated to the VM in VirtualBox:
  1. Select the VM and click "Settings".
  2. Select "System" > "Motherboard" and increase the "Base Memory" to 8 GB.
  3. Select "System" > "Processor" and select at least 2 cores.

#### Access
Launch the VM from the sidebar in Virtualbox. The username is **reticle** and the password is **`reticle`**.

#### Troubleshooting
<details>
<summary>Common VM problems [click to expand]</summary>

 - **Running out of disk space while installing Vivado tools**. The Vivado installer will sometimes
 crash or not start if there is not enough disk space. The Virtual Machine is configured to use
 a dynamically sized disk, so to solve this problem, simply clear space on the host machine. You need about 65 GB of free space.
 - **Running out of memory**. Vivado uses fair amount of memory. If there is not enough memory available to the VM, they will crash and data won't be generated. If something fails, you should increase the RAM and re-try the script that had a failure.
 - **Kernel driver not installed (error "rc=-1908")**. If you're running VirtualBox for the first time on OSX, you may need to [set proper permissions](https://www.howtogeek.com/658047/how-to-fix-virtualboxs-“kernel-driver-not-installed-rc-1908-error/).
</details>


### Building and installing Reticle (2-5 min)

1. Open a terminal.
2. Run `cd ~/Desktop/reticle-evaluation` to go to the evaluation repository.
3. Update the repository by running `git pull`.
4. Run `bash scripts/install_reticle.sh`, which will build and install Reticle.

### [Optional] Opening the README within the VM (1 min)
If you would like to view these instructions from within your VM for simpler back-and-forth viewing (and to simplify copying and pasting commands), we recommend opening the [github link](https://github.com/vegaluisjose/reticle-evaluation) to see the formatted markdown from within the VM.
You can do this by opening the README with `less README.md`, right-clicking the github link, and selecting "open link".

### Try Reticle (2-5 min)
In this section, we will use a short Python script to generate Reticle program, synthesize them, and then output structural Verilog.

The program `scripts/generator.py` will produce Reticle programs that perform a tensor add. It can be run with the following options:
 - `-p [lut-scalar | dsp-vector]` specifies whether to annotate the Reticle instructions for LUT or DSP usage;
 - `-l N`  indicates how long the tensors are;
 - `-o file` writes the output Reticle program to the indicated file.

We recommend comparing LUT vs DSP usage for the same sized program with the following:
`python3 scripts/generator.py -p lut-scalar -l 8 -o lut.ir` to generate a program using LUTs, and
`python3 scripts/generator.py -p dsp-vector -l 8 -o dsp.ir` to generate a program using DSPs.

Feel free to generate some other Reticle programs with different options and take a look at the output. 
Note that the DSP version of the program takes advantage of vectorization to pack four 8-bit additions into each DSP.

Next, we'll use the `reticle-translate` command to synthesize each Reticle program and output structural Verilog. To synthesize the two programs we just generated, run
`reticle-translate lut.ir --fromto ir-to-struct -o lut.v` and
`reticle-translate dsp.ir --fromto ir-to-struct -o dsp.v`.

Take a look at the generated Verilog, but be warned --- it's very low-level! At this point, all operations have been synthesized to primitive FPGA instructions; the "compute" operations in the Verilog are either configuring a LUT or DSP.




### Add a new instruction to the FPGA target (2-5 min)
In this section you will add a new instruction to a target description and compile a program using the new instruction.

Reticle uses `.tdl` files ("target description language") to specify instructions for a given target. Each instruction needs two things:
 - a pattern that can be used in the IR, and
 - an implementation in low-level Reticle assembly.

We will add a "subtract" instruction to the target that uses a LUT.

1. Open the file located in `~/Desktop/reticle-evaluation/reticle/examples/target/ultrascale/lut.tdl`
2. Add the pattern (pat) and implementation (imp) as:

```
pat lut_sub_i8[lut, 1, 2](a: i8, b: i8, en: bool) -> (y: i8) {
    y:i8 = sub(a, b);
}

imp lut_sub_i8[x, y](a: i8, b: i8, en: bool) -> (y: i8) {
    t0:bool = ext[0](a);
    t1:bool = ext[1](a);
    t2:bool = ext[2](a);
    t3:bool = ext[3](a);
    t4:bool = ext[4](a);
    t5:bool = ext[5](a);
    t6:bool = ext[6](a);
    t7:bool = ext[7](a);
    t8:bool = ext[0](b);
    t9:bool = ext[1](b);
    t10:bool = ext[2](b);
    t11:bool = ext[3](b);
    t12:bool = ext[4](b);
    t13:bool = ext[5](b);
    t14:bool = ext[6](b);
    t15:bool = ext[7](b);
    t16:bool = lut2[tbl=9](t0, t8) @a6lut(x, y);
    t17:bool = lut2[tbl=9](t1, t9) @b6lut(x, y);
    t18:bool = lut2[tbl=9](t2, t10) @c6lut(x, y);
    t19:bool = lut2[tbl=9](t3, t11) @d6lut(x, y);
    t20:bool = lut2[tbl=9](t4, t12) @e6lut(x, y);
    t21:bool = lut2[tbl=9](t5, t13) @f6lut(x, y);
    t22:bool = lut2[tbl=9](t6, t14) @g6lut(x, y);
    t23:bool = lut2[tbl=9](t7, t15) @h6lut(x, y);
    t24:bool = vcc();
    t25:bool = gnd();
    t26:i8 = cat(t16,t17,t18,t19,t20,t21,t22,t23);
    y:i8 = carry(a, t26, t24, t25) @carry8(x, y);
}
```
3. Build and install Reticle to apply the changes:
```bash
cd ~/Desktop/reticle-evaluation/reticle
cargo build --release
cargo install --bin reticle-translate --bin reticle-optimize --bin reticle-place --path .
cd ..
```

4. Create a program that uses the `sub` instruction and save it as `prog.ir`:
```
def main(a: i8, b: i8, en: bool) -> (y: i8) {
    y:i8 = sub(a, b);
}
```

5. Compile the program to structural verilog:
```
reticle-translate prog.ir --fromto ir-to-struct -o prog.v
```

 6. Open the resulting Verilog file to see the result.


#### Evaluating Paper Claims
 -  ***Claim E:** Reticle is extensible for new instructions/resources*  
Because Reticle is built around an abstraction of *instructions*, rather transistors or basic logic, its compiler infrastructure can easily express, target, and compile to new FPGA units without resorting to complex inference or unbounded logic synthesis.

## Step-by-Step Guide

The goal of this section is to reproduce all of the evaluation figures included in the paper.

### Installing Xilinx Vivado (Estimated time: 2-4 hours)
Our evaluation uses Xilinx's Vivado tools to generate area and resource estimates. Unfortunately, due to licensing restrictions, we can't distribute the VM with these tools installed. However, the tools are freely available and below are instructions on how to install them.

Our evaluation requires **Vivado WebPACK v.2020.1**. Due to the instability of synthesis tools, we cannot guarantee our evaluation works with a newer or older version of the Vivado tools.

If you're installing the tools on your own machine instead of the VM, you can
[download the Linux installer](https://www.xilinx.com/member/forms/download/xef.html?filename=Xilinx_Unified_2020.1_0602_1208_Lin64.bin).


The following instructions assume you're using the supplied VM:

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
12. Install.  Depending on the speed of your connection, the whole process should take about 2 - 4 hrs.
    

### Reinstall Reticle
Because we modified part of the target description files in the "Getting Started" guide, this may affect the results. To restore the artifact version of the compiler, re-run `bash scripts/install_reticle.sh` from the `reticle-evaluation` directory. 
**Note: this will delete all changes you may have made to Reticle and all files in the `reticle` directory.**

### Generate Figures with Paper Results
Within the `reticle-evaluation` repo, the script `analysis/artifact.ipynb` will generate all the figures from the paper. First try running it on the *existing* data with
`jupyter lab analysis/artifact.ipynb`.
Scroll to the bottom to see the figures.

### Generate the Data (1-2 hours)

The following commands generate the data used by the Jupyter notebook plotting script to plot the figures.

To re-create all the data:

* Generate the compiler run-time data with `python3 scripts/compiler_runtime.py`
* Generate the program run-time and resource usage data with `python3 scripts/program_metrics.py`
* The new data files (csv) should be in `data` directory. Run `git diff` to see the changes in the new data files compared to the committed ones.

### Generate Figures with New (Artifact) Results

Run `jupyter lab analysis/artifact.ipynb` to see the graphs.

#### Evaluating Paper Claims
For the following, please refer to the figures generated for the `tensoradd` example (those following the line `plot_prog("tadd")` in the Jupyter notebook).

 - ***Claim A:** Reticle is faster (up to 100x) synthesizing the same design*  
The first graph shows how long the Reticle compiler took compared to Xilinx Vivado. Note that we are only comparing synthesis time (not placement and routing). Reticle always runs faster than Vivado, outperforming it by over 100x in the best case. We see similar results for the other two examples (`tensordot` and `fsm`). Notably, using Verilog with DSP hints (the middle case, labelled "hint") actually slows down Vivado compared to the baseline for this example.
 - ***Claim B:** Reticle is more predictable*  
The last two graphs in the row display the LUT resources used and the DSP resources used for each case. All three cases use more resources as we make the design larger; however, the Reticle case *only* uses DSPs (its entry in the LUT graph is zero for all sizes). The "hint" case (Verilog + DSP hints in Vivado), despite the annotation to use DSPs, still resorts to using LUTs in some cases --- this is because such annotations are treated as *suggestions*, not *constraints*. When one uses a particular annotation in Reticle (LUT vs DSP), it will always synthesize to the indicated resource (or fail if unavailable).
 - ***Claim C:** Reticle more efficiently exploits DSPs by using value types*  
The final graph ("DSPs used") shows that Reticle uses fewer DSPs than Vivado, despite synthesizing the same design. This follows from Reticle's inclusion of value types, allowing native expression of vectors and exploitation of DSP vectorization capabilities.
 - ***Claim D:** Reticle produces potentially faster designs from better DSP usage*  
It is well understood that DSPs can be faster than LUTs for the same computation. The second graph ("Run-time speedup") shows the runtime performance of the design for each case post-synthesis. Depending on example and design size, Reticle produces a design that is at, near, or faster than the one produced by Vivado --- even when using annotated Verilog.


