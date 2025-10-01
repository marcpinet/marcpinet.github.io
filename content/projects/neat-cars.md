+++
title = "Neat Cars"
description = "🚗 Autonomous vehicle AI agents leveraging NEAT genetic programming and evolutionary reinforcement learning to optimize neural network topologies with real-time visualization and multi-generational evolution."
date = "2023-03-03"
weight = 1

[extra]
remote_image = "/neat-cars/img.gif"
github_link = "https://github.com/marcpinet/neat-cars"
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

# Neat Cars

## 📝 Description

Neat cars allows you to draw a track, choose a starting point and watch the magic happen: the cars will drive themselves and constantly improve their driving skills.
<br>You will also be able to observe the Artificial Neural Network of the best car from the generation.

The project is based on a genetic algorithm called [NEAT (NeuroEvolution of Augmenting Topologies)](https://en.wikipedia.org/wiki/Neuroevolution_of_augmenting_topologies).

## 🎥 Demo

### Live neural network in the top left corner

![demo](https://raw.githubusercontent.com/marcpinet/neat-cars/main/readme-data/nn.gif)

### Track 1: With sensors - Infinite track

<video controls style="max-width: 100%; height: auto;">
    <source src="https://user-images.githubusercontent.com/52708150/223087114-7d4e0401-bb33-46fd-9673-bd973de7235f.mp4" type="video/mp4">
    Your browser does not support the video tag. <a href="https://user-images.githubusercontent.com/52708150/223087114-7d4e0401-bb33-46fd-9673-bd973de7235f.mp4">View video</a>
</video>

### Track 2: Without sensors - Finite track

<video controls style="max-width: 100%; height: auto;">
    <source src="https://user-images.githubusercontent.com/52708150/223087098-0bd16d36-cef2-4773-b657-5471fa1f5baa.mp4" type="video/mp4">
    Your browser does not support the video tag. <a href="https://user-images.githubusercontent.com/52708150/223087098-0bd16d36-cef2-4773-b657-5471fa1f5baa.mp4">View video</a>
</video>

## 💡 How to use

### Prerequisites

* Python 3.7.0+

Get a copy of the Project. Assuming you have git installed, open your Terminal and enter:

```bash
git clone 'https://github.com/marcpinet/neat-cars.git'
```

To install all needed requirements run the following command in the project directory:

```bash
pip install -r requirements.txt
```

### Running

After that, you can proceed to start the program by running `main.py`.

### Controls and tweaks

Instructions are displayed in the window's title.

![title](https://raw.githubusercontent.com/marcpinet/neat-cars/main/readme-data/title1.png)

You can also see the stats of the current generation in the title...

![title2](https://raw.githubusercontent.com/marcpinet/neat-cars/main/readme-data/title2.png)

...and the full stats inside the console.

![cli_output](https://raw.githubusercontent.com/marcpinet/neat-cars/main/readme-data/cli_output.png)

Feel free to tweak the parameters inside the `ai/config.txt` but also the static variables inside the `Car`, `CarAI` and `Engine` classes.
For example, you can disable the rendering of the car's sensors by setting `DRAW_SENSORS` to `False` in the `Car` class.

## ⚙️ How the AI works

The neural network is trained using the NEAT algorithm. The NEAT algorithm is a genetic algorithm which evolves over time from a basic neural network to a more advanced and complex one *depending on your fitness function* by going further and further. Check the [neat-python documentation](https://neat-python.readthedocs.io/en/latest/neat_overview.html) for more infos.

![neat](https://raw.githubusercontent.com/marcpinet/neat-cars/main/readme-data/neat_example.gif)

Also, you can find the full mathematic approach and details directly in the [NEAT paper](https://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf).

### Inputs

The main informations the car will use to drive are the distance to the walls in front and next of it. The car has 5 sensors :

- In front,
- 2 in the diagonals
- 2 on each side

The sensors are represented by a green line in the rendering. Red means the sensor is detecting a wall.

[![inputs](https://raw.githubusercontent.com/marcpinet/neat-cars/main/readme-data/car_sensors.png)](https://marcpinet.me)

### Outputs

The outputs are obviously the car's actions. The car has 4 possible actions:

- Turn left
- Turn right
- Accelerate
- Brake

Note that we have a minimum speed to respect so that the car doesn't stop completely nor drives too slowly.

We get, as a starting point for our neural network, something like this:

![nn](https://raw.githubusercontent.com/marcpinet/neat-cars/main/readme-data/neat_cars_init.png)

The algorithm will then create itself the necessary connections (increasing their weight over time) and eventually add hidden layers in the process.

### Fitness

The fitness is quite simple: the more the car drives, the better it is. The fitness is calculated by the distance the car has driven. The car is therefore penalized if it crashes.

## 🐛 Known issues

* Nothing yet!

## 🥅 TO-DO List

* Find a way to allow 8-like tracks

## ✍️ Authors

* **Marc Pinet** - *Initial work* - [marcpinet](https://github.com/marcpinet)

## 📃 License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/marcpinet/neat-cars/tree/main/LICENSE.md) file for details