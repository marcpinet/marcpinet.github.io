+++
title = "Poubelledroid"
description = "🗑️ An app designed to facilitate the search and cleanup of abandoned waste with a reward system to further engage users in the process."
date = "2023-05-24"
weight = 1

[extra]
remote_image = "/poubelledroid/img.gif"
link_to = "https://github.com/marcpinet/poubelledroid"
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

# Poubelldroid

## 📝 Description

Poubelldroid is a school project for the course *IHM* at Polytech Nice Sophia. an application that aims to facilitate the search and cleanup of abandoned waste.

## 🎥 Demo (censured my home for privacy concerns)

<video controls style="max-width: 100%; height: auto;">
    <source src="https://github.com/user-attachments/assets/f87812d3-c284-4a5a-b68a-ae1cb6de17aa" type="video/mp4">
    Your browser does not support the video tag. <a href="https://github.com/user-attachments/assets/f87812d3-c284-4a5a-b68a-ae1cb6de17aa">View video</a>
</video>

<div class="github-alert github-alert-note" style="border-left: 4px solid #0969da; background-color: #0969da10; padding: 12px 16px; margin: 16px 0; border-radius: 6px;">

<div style="display: flex; align-items: flex-start;">
        <span style="margin-right: 8px; font-size: 16px;">💡</span>

<div style="flex: 1;">
            <strong style="color: #0969da; text-transform: uppercase; font-size: 14px; font-weight: 600;">NOTE</strong>

<div style="margin-top: 4px;"><p>Demo is not the latest version which includes better aestetic, visuals, settings and much more! (see below)</p></div>
        </div>
    </div>
</div>

![Untitled](https://raw.githubusercontent.com/marcpinet/poubelledroid/main/./readme-data/img.png)

## 💡 How to use

### Prerequisites

* [Java JDK 8+](https://www.oracle.com/java/technologies/downloads/) *(tested on 8, 11, and 17)*
* [Android SDK (API 29+)](https://developer.android.com/studio) linked to an `ANDROID_HOME` environement variable *(when opened with Android Studio, the Android SDK is automatically set for you thanks to the `local.properties` auto-generated file)*

1. Get a copy of the Project. Assuming you have git installed, open your Terminal and enter:

    ```bash
    git clone 'https://github.com/marcpinet/poubelledroid'
    ```

2. Setting up your own backend

    2.1 Create a `.env` file at the root directory based on the `.env.template` file

    2.2 Firebase setup

    - Get your own `google-service.json`, set up your own Firebase instance, enable **Firestore**, **Storage**, **Functions** and **Cloud Messaging**

    - Fill the dedicated part in the `.env` file

    - Add the functions from the `firebase-functions` directory using `firebase init` and `firebase deploy` (install using `npm install -g firebase-tools`)

    2.3 Get a **Google Maps API Key** and fill the `.env` file

    2.4 Get a **Twitter API Key (the Bearer Token)** and fill the `.env` file

3. Go into the project's root directory and run:

    ```bash
    .\gradlew build
    ```

    *Note: On Linux, you'll need to use* `chmod +x gradlew` *and* `./gradlew build`

### Running

* If you want to run it in **Android Studio**:
    - Open the folder with Android Studio (choose API 29 if prompted to choose one)
    - Create a new virtual device (take whatever model you want, but we went for the Pixel 2)
    - Use API 29 (Android Q == Android 10)
    - Build and run!

* If you want to run it on **your phone**:
    - Connect your device via debugging mode
    - Paire device with Android Studio using either Wi-Fi debugging or USB Debugging

    OR

    - Build > Generate Signed APK and generate the APK with a certificate
    - Get the APK on your phone by using `adb` or by file transfer
    - Install and run!

## 📃 License

Distributed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/marcpinet/poubelledroid/tree/main/LICENSE) file for details