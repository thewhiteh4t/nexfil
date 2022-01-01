<p align="center"><img src="https://i.imgur.com/Relo42X.jpg"></p>

<p align="center">
    <a href="https://twitter.com/thewhiteh4t">
      <img src="https://img.shields.io/badge/-TWITTER-black?logo=twitter&style=for-the-badge">
    </a>
    &nbsp;
    <a href="https://twc1rcle.com/">
      <img src="https://img.shields.io/badge/-THE WHITE CIRCLE-black?logo=&style=for-the-badge">
    </a>
    &nbsp;
    <a href="https://thewhiteh4t.github.io/">
      <img src="https://img.shields.io/badge/-BLOG-black?logo=dialogflow&style=for-the-badge">
    </a>
</p>

---

**NExfil** is an **OSINT** tool written in python for finding profiles by username. The provided usernames are checked on over 350 websites within few seconds. The goal behind this tool was to get results quickly while maintaining low amounts of false positives.

## Available In

<p align="center">
  <a href="https://blackarch.org/">
    <img width="150px" hspace="10px" src="https://i.imgur.com/YZ5KDL1.png" alt="blackarch finalrecon">
  </a>
</p>

## Featured

* **The Privacy, Security, and OSINT Show**
  * https://soundcloud.com/user-98066669/237-the-huge-osint-show

* **Hakin9 Magazine**
  * https://hakin9.org/product/socmint-for-hackers/

## Features

* **Fast**, lookup can complete **under 20 seconds**
* Over **300** platforms are included
* Batch processing
    * Usernames can be provided from commandline
    * List of usernames can be provided from a file
* Results are automatically saved in txt file
* JSON and CSV file formats [Coming Soon]
* Proxy support [Coming Soon]
* Tor support [Coming Soon]

## Installation

```bash
git clone https://github.com/thewhiteh4t/nexfil.git
cd nexfil
pip3 install -r requirements.txt
```

## Usage

```
usage: nexfil.py [-h] [-u U] [-f F] [-l L] [-t T] [-v] [-U]

nexfil - Find social media profiles on the web | v1.0.1

options:
  -h, --help  show this help message and exit
  -u U        Specify username
  -f F        Specify a file containing username list
  -l L        Specify multiple comma separated usernames
  -t T        Specify timeout [Default : 5]
  -v          Prints version
  -U          Check for Updates
```
> Single username

```bash
python3 nexfil.py -u username
```

> Multiple *comma* separated usernames

```bash
python3 nexfil.py -l "user1,user2"
```

> Username list in a file

```bash
python3 nexfil.py -f users.txt
```

## Demo

### v1.0.0
![](https://raw.githubusercontent.com/thewhiteh4t/static_files/main/nexfil.gif)
