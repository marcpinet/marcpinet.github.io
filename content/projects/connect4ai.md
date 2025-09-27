+++
title = "Connect4 AI"
description = "🤖 A simple and extensible Connect4 with graphical user interface where you can play against an AI (Minimax with Alpha Beta Pruning)."
date = "2023-02-18"
weight = 1

[extra]
remote_image = "/connect4ai/img.gif"
link_to = "https://github.com/marcpinet/connect4-ai"
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

## 📝 Description

A simple Connect4 made with C++ and SFML for the window.
Currently, only the Minimax with Alpha Beta Pruning is implemented.
Maybe, in the future, I'll implement other algorithms if I want to (such as MCTS?).

## 🎥 Demo Minimax with Alpha Beta Pruning

https://user-images.githubusercontent.com/52708150/219687697-d5a2e5b7-3d84-40cd-907d-4ee64157e32d.mp4

## 💡 How to use

### 🪟 Windows

If you've a C/C++ IDE, you should already have `cmake` and `gcc`/`g++`. If not, then install CMake [here](https://cmake.org/download/) and gcc/g++ [here](https://www.devdungeon.com/content/install-gcc-compiler-windows-msys2-cc).

1. Clone the repository

```bash
git clone https://github.com/marcpinet/connect4-ai
```

2. Initialize the SFML submodule

```bash
git submodule update --init --recursive
```

3. Build with CMake

```bash
cmake -S . -B output -DCMAKE_BUILD_TYPE=Release -G"MinGW Makefiles"
```

4. Build the project using make inside the newly created output folder

```bash
cd output && make
```

5. Run the `.exe`

### 🐧 Linux / WSL

1. Run the holy command

```bash
sudo apt-get update
```

2. Install the following packages

```bash
sudo apt install libsfml-dev gdb cmake build-essential libvorbis-dev libopenal-dev freetype2-demos libudev-dev libx11-dev libxrandr-dev
```

3. Clone the repository

```bash
git clone https://github.com/marcpinet/connect4-ai
```

4. Initialize the SFML submodule

```bash
git submodule update --init --recursive
```

5. Build with CMake

```bash
cmake -S . -B output -DCMAKE_BUILD_TYPE=Release
```

6. Build the project using make inside the newly created output folder

```bash
cd output && cp -r ../assets assets && make
```

7. Run the file!

```bash
chmod u+x Connect4_AI && ./Connect4_AI
```

## 📄 Note

On Windows, it will probably be easier to run the project using an IDE such as [CLion](https://www.jetbrains.com/clion/).

No cache issue.