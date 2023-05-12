# LONS-C2
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=green) \
![Banner](https://github.com/m4riio21/LONS-C2/blob/e275c02506acca5d114b07dbff4a498124173bb4/resources/LOGO.png)


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Usage](#usage)


## Introduction
**Listener-Oriented Network Server (LONS)** is a socket-based command and control server, designed to allow pentesters and security enthusiasts to centralize and manage in an easy manner terminal sessions in different machines.

## Features

- Simple CLI with client selection
- Easy to use
- Running commands in remote clients
- Retrieve network information
- Upload files to clients
- Retrieve files from clients
- Take screenshots from clients and visualize them

## Usage

### Server

Default port is 1337. User may specify a custom port
```shell
$ python main.py [port]
```

### Client

```shell
$ python main.py <server_ip> <server_port>
```

