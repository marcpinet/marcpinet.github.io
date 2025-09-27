+++
title = "Parm"
description = "🧀 PARM (Polytech ARM-based embedded processor), ARMv7-Compatible CPU in Logisim with Custom Assembler and C-to-Assembly Toolchain for Embedded Systems Simulation."
date = "2023-01-30"
weight = 1

[extra]
remote_image = "/parm/img.gif"
link_to = "https://github.com/marcpinet/parm"
+++

<style>
/* GitHub Alert Styles */
.github-alert {
    border-radius: 6px;
    margin: 16px 0;
    padding: 12px 16px;
    border-left: 4px solid;
}

.github-alert-note {
    background-color: #ddf4ff;
    border-color: #0969da;
}

.github-alert-tip {
    background-color: #dcfce7;
    border-color: #1a7f37;
}

.github-alert-important {
    background-color: #f3e8ff;
    border-color: #8250df;
}

.github-alert-warning {
    background-color: #fff8dc;
    border-color: #d1242f;
}

.github-alert-caution {
    background-color: #ffebee;
    border-color: #d1242f;
}

/* Table Wrapper */
.table-wrapper {
    overflow-x: auto;
    margin: 16px 0;
}

.table-wrapper table {
    width: 100%;
    border-collapse: collapse;
}

.table-wrapper th,
.table-wrapper td {
    border: 1px solid #d1d5da;
    padding: 8px 12px;
    text-align: left;
}

.table-wrapper th {
    background-color: #f6f8fa;
    font-weight: 600;
}

/* Video Styles */
video {
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    margin: 16px 0;
}

/* Code Block Styles */
pre {
    background-color: #f6f8fa;
    border-radius: 6px;
    padding: 16px;
    overflow-x: auto;
    margin: 16px 0;
}

code {
    background-color: #f6f8fa;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'SFMono-Regular', 'Monaco', 'Inconsolata', 'Liberation Mono', 'Consolas', monospace;
    font-size: 85%;
    color: #24292f;
}

pre code {
    background-color: transparent;
    padding: 0;
}

/* Dark mode support for inline code */
@media (prefers-color-scheme: dark) {
    pre {
        background-color: #161b22;
        color: #f0f6fc;
    }
    
    code {
        background-color: #21262d;
        color: #f0f6fc;
    }
    
    pre code {
        background-color: transparent;
        color: inherit;
    }
}
</style>

# Polytech ARM-based embedded processor

## 📋 Instructions we had to follow

By using [Logisim](https://github.com/marcpinet/parm/tree/main/proc/logisim/), we firstly had to make a [CPU](https://github.com/marcpinet/parm/tree/main/proc/) (a simplified one) which can run binary files (machine code). You can find how to convert Clang files into Assembly files in the next section. Next, we had to make [a program](https://github.com/marcpinet/parm/tree/main/asm/) which can translate assembly language (ARMv7) into machine code.

You can learn more about Logisim, ARMv7 and the whole Cortex-M0 family of processors in the [docs](https://github.com/marcpinet/parm/tree/main/docs/) folder.

## ⚙️ Compile C to ARM Assembly using the CPU

To check whether our CPU works or not, we need to compile these C programs and compare each other.

Install the `libc6-armel-cross`, `libc6-dev-armel-cross`, `binutils-arm-linux-gnueabi` and `libncurses5-dev` packages by using the following command:

```bash
sudo apt-get install clang libc6-armel-cross libc6-dev-armel-cross binutils-arm-linux-gnueabi libncurses5-dev
```

Then, install `gcc` and `g++` to support ARM:

```bash
sudo apt-get install gcc-arm-linux-gnueabi g++-arm-linux-gnueabi
```

Finally, you can compile like this:

```bash
clang -S -target arm-none-eabi -mcpu=cortex-m0 -O0 -mthumb -nostdlib -I./include main.c
```

Please, note that the `./include` folder (which contains the headers) should be in the same directory of the `main.c`.
You can see some examples in the [c](https://github.com/marcpinet/parm/tree/main/c/) folder.

## 📽️ Presentation

See the [presentation](https://github.com/marcpinet/parm/tree/main/presentation/) folder for more details.

## 🧾 Additional informations

### C Headers

<div class="table-wrapper">
| Program | Description |
|-|-|
| crypto | Cryptography |
| fixed | Fixed Point Decimal Numbers |
| math | Mathematical tools |
| parm | Main Header |
| stdio | Text Input/Output (keyboard, terminal) |
| string | Basic implementation of strings |
| string2 | Other basic implementation of strings |
| trigo | Trigonometric functions (Taylor series) |
| utils | Debugging Tools |
| video | Matrix screen |
</div>

### C programs

<div class="table-wrapper">
| Program | Description |
|-|-|
| calckeyb| Calculator with keyboard and terminal |
| calculator | Calculator with DIP-switches |
| simple_add | Adds two variables and displays it in RES |
| testfp | Demonstrate fixed-point number macros |
| tty | Display "Project PARM" in terminal |
</div>

### MMIO

See `parm.h` for the pins documentation.

## ✒️ Authors

* Marc PINET - [marcpinet](https://github.com/marcpinet)
* Loïc PANTANO - [loicpantano](https://github.com/loicpantano)
* Arthur RODRIGUEZ - [rodriguezarthur](https://github.com/rodriguezarthur)