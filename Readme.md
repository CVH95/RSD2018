# RSD MES SYSTEM

RESTful API designed for the project in the course Robot Systems Design (University of Southern Denmark). This repository only contains the MES client. Cell number: 3.

## 1. Specifications

**Software requirments:**

 - Python3 venv virtual environment to run the server.
 - Python Flask, and its Flask-MySQL extension for running the server.
 - MySQL.
 - Flask SQL-alchemy.
 - Python Requests and PyMySQL for the client side.
 
 **Project Organization:**
 
 - _Client\_rpi\_version_ directory.
     - mes\_api.py
     - feedback\_api.py
     - mes\_client.py
     - initia.py
 - _PLC/_ directory.
     - plc\_fake\_server.py
 - _Scripts/_ directory.
     - run\_workcell.sh
     - test\_connectivity.sh
 - _Utils/_ directory.
     - DELETE\_realDB\_test.py
     
## 2. Quick Guide

### 2.1. Install

On the Pi:

```sh
$ mkdir Workspace
$ cd Workspace/
$ git clone <repo_url> RSD2018
$ mv RSD2018/RSD2018/Scripts/run_workcell.sh ~/Desktop
$ mv RSD2018/RSD2018/Scripts/test_connectivity.sh ~/Desktop
```

Now change permissions on the scripts:

```sh
$ sudo chmod +x ~/Desktop/run_workcell.sh
$ sudo chmod +x ~/Desktop/test_connectivity.sh
```

### 2.2. Usage

 - **General:**

To make an initial network test run the `test_connectivity.sh` script. To run the workcell use `run_workcell.sh`.

 - **Code:**

In the _Client\_rpi\_version_  directory, _mes\_api.py_ and _feedback\_api.py_ are the main function collection. The feedback (email) is disabled by default. If you want to use it, uncomment the lines related to it in th emain program: _mes\_client.py_. The script _initia.py_ is the source of the connectivity test.

 - **Develope mode:**

While developing, if the PLC is not available yet, the script  _PLC/plc\_fake\_server.py_ simulates the PLC's routine. Change its IP address to localhost if tested on the same machine as the client or with the computer's IP if the client is being tested from the RPi.

The srcipt _Utils/DELETE\_realDB\_test.py_ can be used to flush taken orders that remain in teh database because the main program could not delete them. Enter the order's id and ticket in the code to remove them.

## Note

For more details on the project, go to the [Wiki](https://github.com/CVH95/RSD2018/wiki).

## Authors

Group 3, Robot System Design 2018:

 - Carlos Viescas
 - Carolin Nowak
 - Daniel Holst Hviid

University of Southern Denmark.

## References

 - Flask [Installation](http://flask.pocoo.org/docs/1.0/installation/#python-version).
 - Flask [Quickstart](http://flask.pocoo.org/docs/1.0/quickstart/).
 - [PyMySQL](https://pymysql.readthedocs.io/en/latest/user/examples.html) examples.
 - [Flask-MySQL](https://flask-mysql.readthedocs.io/en/latest/) extension.
 - Creating a WebApp from scratch using Python Flask and MySQL [tutorial](https://code.tutsplus.com/es/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972).
 - [Simultaneous WiFi and Ethernet access](http://www.knight-of-pi.org/setup-simultanous-ethernet-and-wifi-access-for-the-raspberry-pi-3/) for Raspberry Pi.
 - [Send emails](https://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email) with Python.
 - Run bash script from desktop [icon](http://www.raspberry-projects.com/pi/pi-operating-systems/raspbian/gui/desktop-shortcuts).