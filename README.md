<p align="center"><img src="https://i.imgur.com/Relo42X.jpg"></p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3.9-brightgreen.svg?style=plastic">
<img src="https://img.shields.io/badge/OSINT-red.svg?style=plastic">

<p align="center">
    <a href="https://twitter.com/thewhiteh4t"><b>Twitter</b></a>
    <span> - </span>
    <a href="https://discord.gg/UM92zUn"><b>Discord</b></a>
    <span> - </span>
    <a href="https://thewhiteh4t.github.io/"><b>thewhiteh4t's Blog</b></a>
</p>

---

**NExfil** is an **OSINT** tool written in python for finding profiles by username. The provided usernames are checked on over 350 websites within few seconds. The goal behind this tool was to get results quickly while maintaining low amounts of false positives.

If you like my work please **star** this project :D

If you find any errors or false positives or if you want to suggest more websites feel free to open an issue.

## Features

* **Fast**, lookup can complete **under 20 seconds**
* Over **350** platforms are included
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

```bash
python3 nexfil.py -h
usage: nexfil.py [-h] [-u U] [-d D [D ...]] [-f F] [-l L] [-t T] [-v]

nexfil - Find social media profiles on the web | v1.0.0

optional arguments:
  -h, --help    show this help message and exit
  -u U          Specify username
  -d D [D ...]  Specify DNS Servers [Default : 1.1.1.1]
  -f F          Specify a file containing username list
  -l L          Specify multiple comma separated usernames
  -t T          Specify timeout [Default : 20]
  -v            Prints version

# Single username
python3 nexfil.py -u username

# Multiple *comma* separated usernames
python3 nexfil.py -l "user1, user2"

# Username list in a file
python3 nexfil.py -f users.txt
```

## Demo

### v1.0.0
![](https://raw.githubusercontent.com/thewhiteh4t/static_files/main/nexfil.gif)
