+++
title = "Sort Visualizer"
description = "🧮 A simple sorting algorithm visualizer (with a lot of algorithms to observe). You can also adjust the size of the array to be sorted and much more!"
date = "2022-03-18"
weight = 1

[extra]
remote_image = "/sort_visualizer/img.gif"
link_to = "https://github.com/marcpinet/sort-visualizer"
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

# Sorting Visualizer

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg) [![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://GitHub.com/Naereen/ama)

A simple graphical sorter written in Python with Pygame where you can visualize many algorithms and see how they actually work.

You can adjust the speed using <kbd>→</kbd> or <kbd>←</kbd> and shuffle the array at the end of the sorting to restart the algorithm by pressing <kbd>SPACE</kbd>. Finally, press <kbd>ESC</kbd> to exit.

I will add more algorithms when I have time.

## How to use

Just launch the `main.py`, choose your algorithm and the size of the array to sort.
When the Pygame window gets opened, press <kbd>SPACE</kbd> to start the algorithm.

## Known issues

<ul>
    <li>Nothing yet!</li>
</ul>

## Demo

### Quick Sort - Randomized Array

https://user-images.githubusercontent.com/52708150/158039436-4f7f3847-20ff-4f5f-8981-53d9babdfc36.mp4

### Merge Sort - Randomized Array

https://user-images.githubusercontent.com/52708150/158039423-6e953005-65d8-437c-9da1-f279f738a600.mp4

### Heap Sort - Randomized Array

https://user-images.githubusercontent.com/52708150/158039415-4e5dfd88-dc88-4c53-9f15-f79d7954352d.mp4

## Support 👨‍💻

Any problems with running the script and any questions please create a new issue [here](https://github.com/marcpinet/sorting-visualizer/issues/new?assignees=&labels=&template=bug_report.md&title=).

You can also contribute to this project by requesting new features [here](https://github.com/marcpinet/sorting-visualizer/new?assignees=&labels=&template=feature_request.md&title=).

I never ask for money for my open source projects. However, you can still tip me if you want.
I am a [Brave Verified Creator](https://i.imgur.com/fOUfdM5.png)!

## Prerequisites

* Python 3.7.0+

Get a copy of the Project. Assuming you have git installed, open your Terminal and enter:

```bash
git clone 'https://github.com/marcpinet/sorting-visualizer.git'
```

To install all needed requirements run the following command in the project directory:

```bash
pip install -r requirements.txt
```

## Running 🏃

After that you can proceed to start the program by running `main.py`.

## TO-DO List

<ul>
    <li>Nothing yet.</li>
</ul>

## Authors

* **Marc Pinet** - *Initial work* - [marcpinet](https://github.com/marcpinet)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/marcpinet/sort-visualizer/tree/main/LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used.