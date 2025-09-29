+++
title = "LetsGoBiking"
description = "🚲 Pathfinding for JCDecaux bike sharing systems with optimized server architecture, intelligent caching, distributed proxies, and real-time route calculation."
date = "2023-11-28"
weight = 1

[extra]
remote_image = "/letsgobiking/img.gif"
link_to = "https://github.com/marcpinet/letsgobiking"
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

# LetsGoBiking

## 📝 Description

This project involves the development of a self-hosted SOAP server (with cache, queue and proxy) in C

# and a heavy client in Java for a routing service.

The server interfaces with the JC Decaux API and an external REST API to provide itinerary planning services, while the client application allows users to request and display these itineraries.

The project aims to demonstrate the practical application of SOAP and REST APIs, as well as the integration of various software components into a cohesive system.

This project was developed as part of an advanced IT course, requiring careful planning, understanding of web services, and efficient coding practices.

## 📦 Features

- Enter any place you want from origin to destination 🌎
- Map itinerary visualization 🗺️
- Real time data with live map update 🕒
- Fully GUI-zed 🪟
- Travel is organized from your current location to the nearest station, then from the station closest to your destination to your final destination 📍
- Self-hosted SOAP server in C

# for itinerary planning 🌐
- Java-based heavy client for user interaction and data display 🖥️
- Integration with JCDecaux API and external REST APIs 🚲
- Advanced features like caching and message queuing with ActiveMQ 🚀
- Detailed documentation for installation and usage 📚

## ⚙️ Installation

### Requirements

- Java 11+
- Maven
- .NET Framework 4.8
- ActiveMQ

### Installation and step-by-step setup

<div class="github-alert github-alert-warning" style="border-left: 4px solid #d1242f; background-color: #d1242f10; padding: 12px 16px; margin: 16px 0; border-radius: 6px;">

<div style="display: flex; align-items: flex-start;">
        <span style="margin-right: 8px; font-size: 16px;">⚠️</span>

<div style="flex: 1;">
            <strong style="color: #d1242f; text-transform: uppercase; font-size: 14px; font-weight: 600;">WARNING</strong>

<div style="margin-top: 4px;"><p>Because of Windows 10/11 port access and protected system resources policies, you need to run the servers as administrator to allow them to host the services on <code>localhost</code>. If you don't intend to run the servers elsewhere than from your IDE, make sure to run your IDE as administrator aswell.</p></div>
        </div>
    </div>
</div>
<div class="github-alert github-alert-note" style="border-left: 4px solid #0969da; background-color: #0969da10; padding: 12px 16px; margin: 16px 0; border-radius: 6px;">

<div style="display: flex; align-items: flex-start;">
        <span style="margin-right: 8px; font-size: 16px;">💡</span>

<div style="flex: 1;">
            <strong style="color: #0969da; text-transform: uppercase; font-size: 14px; font-weight: 600;">NOTE</strong>

<div style="margin-top: 4px;"><p>Assuming you've all your path environment variables (<a href="https://visualstudio.microsoft.com/downloads/?cid=learn-onpage-download-cta#build-tools-for-visual-studio-2022">msbuild</a>, <a href="https://www.nuget.org/downloads">nuget</a>, <a href="https://activemq.apache.org/components/classic/download/">activemq</a> and <a href="https://maven.apache.org/download.cgi">mvn</a>), you can directly run the <code>auto_start.bat</code>. Please, don't forget to setup the <code>.env file</code> in <code>/Server/.env</code>.</p></div>
        </div>
    </div>
</div>
1. **Clone** the repository to your local machine.

```bash
git clone https://github.com/marcpinet/letsgobiking.git
```

2. **Create** a `.env` file in `Servers/`, using [.env.example](https://github.com/marcpinet/letsgobiking/tree/main/Servers/.env.example) and fill in the API Keys of [OpenRouteService](https://api.openrouteservice.org/) and [JCDecaux](https://developer.jcdecaux.com/#/home).

3. **Open** an ActiveMQ instance in a terminal. Make sure [you have it installed](https://activemq.apache.org/components/classic/download/) and added to environment variables.

```bash
activemq start
```

4. **Install, Build & Run (as administrator)** the servers using either command line or your preferred IDE (just open the `.sln`).

```bash
cd Servers
nuget restore LetsGoBikingServer.sln
msbuild /p:Configuration=Release /p:TargetFrameworkVersion=v4.8
start "Caching Server" .\CachingServer\bin\Release\CachingServer.exe
start "Proxy Server" .\ProxyServer\bin\Release\ProxyServer.exe
start "Routing Server" .\RoutingServer\bin\Release\RoutingServer.exe
```

5. **Install, Build & Run** the client using either command line or your preferred IDE.

```bash
cd ../Client
mvn clean install
mvn compile
mvn exec:java -Dexec.mainClass="com.polytech.mwsoc.Main"
```

## 💡 How to use

Once you did all the steps above, you'll be prompted to choose a starting place and a destination.

<div class="github-alert github-alert-note" style="border-left: 4px solid #0969da; background-color: #0969da10; padding: 12px 16px; margin: 16px 0; border-radius: 6px;">

<div style="display: flex; align-items: flex-start;">
        <span style="margin-right: 8px; font-size: 16px;">💡</span>

<div style="flex: 1;">
            <strong style="color: #0969da; text-transform: uppercase; font-size: 14px; font-weight: 600;">NOTE</strong>

<div style="margin-top: 4px;"><p>The returned itinerary will <strong>ALWAYS</strong> be the shortest path. If, by walking, you're making it faster rather than by going to a bike station, it will return the walk itinerary instead.</p></div>
        </div>
    </div>
</div>

### Examples

🔵 = JCDecaux bike itinerary
🔴 = Walking itinerary

#### Real Time with live update of the itinerary (with activemq) and steps

<video controls style="max-width: 100%; height: auto;">
    <source src="https://github.com/user-attachments/assets/499d0261-4c13-4cdc-85c1-d8c0d9c8f57c" type="video/mp4">
    Your browser does not support the video tag. <a href="https://github.com/user-attachments/assets/499d0261-4c13-4cdc-85c1-d8c0d9c8f57c">View video</a>
</video>

#### Some map showcases and search addresses (note that you can type whatever you want, not only plain cities)

```
Enter an origin:
montpellier

Enter a destination:
madrid
```

![img1](https://i.imgur.com/FwDwjor.png)

---

```
Enter an origin:
campus sophiatech

Enter a destination:
mouratoglou
```

![img2](https://i.imgur.com/8GWbeXh.png)

## 🐛 Known issues

- The loading indicator doesn't show its label on second invoke (e.g after asking for a second itinerary).

## ✍️ Authors

- Marc Pinet - *Initial work* - [marcpinet](https://github.com/marcpinet)