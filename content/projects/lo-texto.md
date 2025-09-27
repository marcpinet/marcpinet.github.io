+++
title = "LoTexto"
description = "💬 An app made from scratch that allows LoRaWAN communications for emergency messages in Vietnam."
date = "2022-07-01"
weight = 1

[extra]
remote_image = "/lo-texto/img.gif"
link_to = "https://github.com/marcpinet/lo-texto"
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

# Lo-Texto

Development of an emergency app (from scratch) with LoRaWAN protocol. This project was made for an internship purpose at Da Nang in Vietnam.

## Prerequisites

* One or more Arduino Pro or Pro Mini boards
* As much HM-10 BLE Module as you have boards
* Cables to link HM-10 with your boards
* A city where LoRaWAN gateways are available
* A raspberry pi or something like that where a Linux OS is installed, will be used as a server
* Python 3.7.0+ (installed on the server)
* MySQL installed on your server (I used MariaDB), if you want to use something else, do not forget to edit the `main.py` file!

Get a copy of the Project. Assuming you have git installed, open your Terminal and enter:

```bash
git clone 'https://github.com/marcpinet/lo-texto.git'
```

## Authors

* *Lora, Bluetooth and server* - [marcpinet](https://github.com/marcpinet)
* *Devices, TheThingsNetwork and database* - [lyne-ed](https://github.com/lyne-ed)
* *Application backend and Bluetooth communication* - [loicpantano](https://github.com/loicpantano)
* *Application frontend and logo* - [marcusaasjensen](https://github.com/marcusaasjensen)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](https://github.com/marcpinet/lo-texto/tree/main/LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used.