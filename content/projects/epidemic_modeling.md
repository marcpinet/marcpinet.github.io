+++
title = "Epidemic Modeling"
description = "🦠 Python script that simulates a pandemic using moving dots with tweakable parameters and then generates a graph according to obtained values. Validated against research literature with real-time intervention scenario analysis."
date = "2022-01-18"
weight = 1

[extra]
remote_image = "/epidemic_modeling/img.gif"
github_link = "https://github.com/marcpinet/epidemic-modeling"
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

# Epidemic Modeling

🧬 Tweak transmission rate, recovery rate, death rate, number of people, and many more! 🧬

⚙️ Graphical User Interface with sliders and buttons. ⚙️

👁️ Visual and graphical interpretation of results from the simulation 👁️

🔬 Randomized simulation 🔬

🧫 Inspired by [SEIDR Model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology) 🧫

## Features

* Every parameters of the simulation is editable through an interactive GUI 🖥
* Humans are travelling randomly but logically and are represented by dots 👦
* Humans can wear a mask and mask are 80% effective 🧢
* Humans wearing a mask are represented by a "+" and do not easily infect as well as being harder to infect ⛑️
* The simulation is almost fully randomized but keeps logic with given values 🎲
* You can adjust the speed of the simulation with the slider 🏃
* You can tweak some specific parameters of the simulation 🧰
* At the end of the simulation, you can see the evolution of the population through time 📊
* ... and many more! 🎯

## Demo

### One wave of the epidemic was simulated

<video controls style="max-width: 100%; height: auto;">
    <source src="https://user-images.githubusercontent.com/52708150/146844598-e74a4185-b21d-40bf-9046-5e6e4423ef77.mp4" type="video/mp4">
    Your browser does not support the video tag. <a href="https://user-images.githubusercontent.com/52708150/146844598-e74a4185-b21d-40bf-9046-5e6e4423ef77.mp4">View video</a>
</video>

### Three waves of the epidemic were simulated

<video controls style="max-width: 100%; height: auto;">
    <source src="https://user-images.githubusercontent.com/52708150/146844606-71d78f0f-11e3-47e2-8330-953a9d3600f4.mp4" type="video/mp4">
    Your browser does not support the video tag. <a href="https://user-images.githubusercontent.com/52708150/146844606-71d78f0f-11e3-47e2-8330-953a9d3600f4.mp4">View video</a>
</video>

### Masked dots example

<video controls style="max-width: 100%; height: auto;">
    <source src="https://user-images.githubusercontent.com/52708150/146844600-05ff0eda-c5c0-4466-9e31-b50abf161229.mp4" type="video/mp4">
    Your browser does not support the video tag. <a href="https://user-images.githubusercontent.com/52708150/146844600-05ff0eda-c5c0-4466-9e31-b50abf161229.mp4">View video</a>
</video>

### Support 👨‍💻

Any problems with running the script and any questions please create a new issue [here](https://github.com/marcpinet/epidemic-modeling/issues/new?assignees=&labels=&template=bug_report.md&title=).

You can also contribute to this project by requesting new features [here](https://github.com/marcpinet/epidemic-modeling/new?assignees=&labels=&template=feature_request.md&title=).

I never ask for money for my open source projects. However, you can still tip me if you want.
I am a [Brave Verified Creator](https://i.imgur.com/fOUfdM5.png)!

### Prerequisites

* Python 3.7.0+

Get a copy of the Project. Assuming you have git installed, open your Terminal and enter:

```bash
git clone 'https://github.com/marcpinet/epidemic-modeling.git'
```

To install all needed requirements run the following command in the project directory:

```bash
pip install -r requirements.txt
```

## Running 🏃

After that you can proceed to start the program by running `main.py`.

## Authors

* **Marc Pinet** - *Initial work* - [marcpinet](https://github.com/marcpinet)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/marcpinet/epidemic-modeling/tree/main/LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used.

## Contributions

Special thanks to [loicpantano](https://github.com/loicpantano) for some ideas and [marcusaasjensen](https://github.com/marcusaasjensen) for its participation in the project (he made a its own simulation in C

# of an airport with graphs, see [marcus' simulation](https://github.com/marcusaasjensenunice/covid-simulation)).

We were in the same team for this project and we worked together on different programs.