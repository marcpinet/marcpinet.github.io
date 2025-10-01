+++
title = "Handigits"
description = "🖐️ Background-independent deep learning model for hand sign digit recognition. Used my own framework (Neuralnetlib) for model training and inference, and Google MediaPipe for hand tracking and preprocessing"
date = "2024-05-27"
weight = 1

[extra]
remote_image = "/handigits/img.gif"
github_link = "https://github.com/marcpinet/handigits"
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

# Handigits

## 📝 Description

The goal of this project was to make a deep learning model that could recognize hand signs digits, no matter the environment.

<div class="github-alert github-alert-tip" style="border-left: 4px solid #1a7f37; background-color: #1a7f3710; padding: 12px 16px; margin: 16px 0; border-radius: 6px;">

<div style="display: flex; align-items: flex-start;">
        <span style="margin-right: 8px; font-size: 16px;">💡</span>

<div style="flex: 1;">
            <strong style="color: #1a7f37; text-transform: uppercase; font-size: 14px; font-weight: 600;">TIP</strong>

<div style="margin-top: 4px;"><p>NEW: The project now uses <a href="https://github.com/marcpinet/neuralnetlib">Neuralnetlib, my own deep learning framework</a> instead of TensorFlow and Keras!</p></div>
        </div>
    </div>
</div>
Every information you need is in the source code, but here are some important points:

- The dataset used is: [Sign-Language-Digits-Dataset](https://github.com/ardamavi/Sign-Language-Digits-Dataset)
- The library I use to detect the hand is: [mediapipe](https://github.com/google-ai-edge/mediapipe)

I don't think this project deserves a bigger README, like my other projects.

It was primarily made for fun and to learn more about real-time processing and deep learning.

## 🎥 Demo

![demo](https://raw.githubusercontent.com/marcpinet/handigits/main/resources/demo.gif)

## 💡 How to use

### Prerequisites

* Python 3.7.0+

Get a copy of the Project. Assuming you have git installed, open your Terminal and enter:

```bash
git clone 'https://github.com/marcpinet/handigits'
```

To install all needed requirements run the following command in the project directory:

```bash
pip install -r requirements.txt
```

### Running

After that, you can proceed to start the program by running `main.py`.

## 🐛 Known issues

* Nothing yet!

## 🥅 TO-DO List

* Nothing yet!

## ✍️ Authors

* **Marc Pinet** - *Initial work* - [marcpinet](https://github.com/marcpinet)

## 📃 License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/marcpinet/handigits/tree/main/LICENSE.md) file for details