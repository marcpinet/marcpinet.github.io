+++
title = "Quanridor"
description = "♟️ Quoridor game, enhanced with fog of war, available for both web and mobile platforms (with bots and online support) using only pure HTML CSS & Javascript."
date = "2024-04-06"
weight = 1

[extra]
remote_image = "/quanridor/img.gif"
link_to = "https://github.com/marcpinet/quanridor"
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

![quanridor](https://raw.githubusercontent.com/marcpinet/quanridor/main/readme-assets/quanridor-title.png)

### Showcase

#### PC version (very fast, not showing every single details...)

https://github.com/marcpinet/quanridor/assets/52708150/8aa827ca-f739-4675-a9a9-6386ea3f930d

#### Mobile version (same, but you can see me playing online)

https://github.com/marcpinet/quanridor/assets/52708150/9ef180f8-7e02-4061-984a-86cdffe0278c

## 🌐 Hosting

You can access the project by visiting: [http://quanridor.ps8.academy/](http://quanridor.ps8.academy/)

_Unless I forgot to pay the bill, in which case you can still run the project locally by following the instructions below_

## 📝 Description

Quoridor game, available for both web and mobile platforms (with bots and online support) using only pure HTML CSS & Javascript. Made as part as a school project

This version of the game includes a [fog of war](https://en.wikipedia.org/wiki/Fog_of_war) system, which means that you can only see the tiles that are in your line of sight. This adds a whole new layer of strategy to the game, as you can't see the other player's moves until you're close enough to them.

The whole solution will be a fully working version of the game where you can play online against your friends or against an AI with multiple levels of difficulty.

There's also a chat system, emote system, leaderboard, statistics, and much more.

## 📦 Features (W.I.P)

- Minimalistic and clean UI/UX design 🖥️
- Login / Register system with secure backend 📝
- Token authentication system (JWT) 🍪
- In-progress game listing 📋
- Play locally with someone else 🎮
- Play against bots with different levels of difficulty 🤖
- Leaving a game? No problem, it's in our database, waiting for you to join back! 📂
- Multiplayer online games with friends or random people 🌐
- Social system (friends, chat, emotes, notifications, etc.) 📱
- Challenge your friends to a duel! 🤺
- Leaderboard with elo 🏆
- Compatibility with mobile devices 📱

## ⚙️ Local installation

### Requirements

- Node.js 18+
- Docker
- Cordova (only if you want to run the mobile version)

### Setup

#### For PC

1. **Clone** the repository to your local machine.

   ```bash
   git clone https://github.com/PolytechNS/ps8-24-quanridor.git
   ```

2. _(Optional)_ **Install** the dependencies for development puroposes.

   ```bash
   npm install
   ```

3. **Build and run** the backend using Docker.

   ```bash
   docker compose up -d
   ```

4. Run the frontend by going to [http://localhost:8000](http://localhost:8000) in your browser.

5. **Play**!

<div class="github-alert github-alert-note" style="border-left: 4px solid #0969da; background-color: #0969da10; padding: 12px 16px; margin: 16px 0; border-radius: 6px;">

<div style="display: flex; align-items: flex-start;">
        <span style="margin-right: 8px; font-size: 16px;">💡</span>

<div style="flex: 1;">
            <strong style="color: #0969da; text-transform: uppercase; font-size: 14px; font-weight: 600;">NOTE</strong>

<div style="margin-top: 4px;">The only libraries required for the backend to work are `mongodb`, `nodemon`, `socket.io`, `jsonwebtoken` and `bcrypt`.
There's also `husky` to enforce the use of `prettier` on every commit (and also for DevOps purposes)</div>
        </div>
    </div>
</div>

#### For mobile

1. Make sure you have Cordova correctly installed and configured (see [Cordova's documentation](https://cordova.apache.org/docs/en/11.x/guide/platforms/android/)).

2. Run `build-apk.py`

3. **Run** the app on your mobile device.

   ```bash
   cordova run android
   ```

4. **Play**!

## 💡 How to use

Create an account and play!

There is a mock account already created for you to test the game:

- **Username**: `admin`
- **Password**: `admin`

... 👀

## 🐛 Known issues

- Nothing yet!

## ✍️ Authors

- Marc Pinet - _Initial work_ - [marcpinet](https://github.com/marcpinet)
- Arthur Rodriguez - _Initial work_ - [rodriguezarthur](https://github.com/rodriguezarthur)
- Marcus Aas Jensen - _Initial work_ - [marcusaasjensen](https://github.com/marcusaasjensen)
- Loris Drid - _Initial work_ - [lorisdrid](https://github.com/LorisDrid)