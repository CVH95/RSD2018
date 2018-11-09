# RSD MES SYSTEM

## 1. Server 

The MES system is made in Python3 and are using Flask with a SQL extension for the REST api.

The system also need a MySQL v8 db to run. 

Included are a python file for the Flask server and a SQL export, that shows the structure of the "rsd" SQL db.

In the Python code you can see the configuration for the database in order for the python code to access the SQL db.

Note: the MES server will automatic add more jobs, when they are below 5. This is just a sample code - the final system have another behavior, but this shows the idea.

[Note provided in the lecture]

### 1.1. Setting up

 - **Install Flask:**

 Create virtual environment:

 ```sh
 $ sudo apt-get install python3-venv
 $ python3 -m venv venv
 ```

 Activate virtual environment and install Flask:

 ```sh 
 $ . venv/bin/activate
 $ pip install --upgrade pip
 $ pip install Flask
 ```
 - **Install Flask-MySQL extension:**

 In the virtual environment run:

 ```sh
 $ pip install flask-mysql
 $ pip show flask-mysql

 Name: Flask-MySQL
 Version: 1.4.0
 Summary: Flask simple mysql client
 Home-page: https://github.com/cyberdelia/flask-mysql/
 Author: Timothee Peignier
 Author-email: timothee.peignier@tryphon.org
 License: BSD
 Location: /.../RSD2018/RSD2018/Server/venv/lib/python3. 5/site-packages
 Requires: Flask, PyMySQL
 Required-by: 
 ```

 - **Install SQL-alchemy by Flask:**
 
 In the virtual environment:

 ```sh
 $ pip install flask-sqalchemy
 $ pip show sqlalchemy

 Name: SQLAlchemy
 Version: 1.2.13
 Summary: Database Abstraction Library
 Home-page: http://www.sqlalchemy.org
 Author: Mike Bayer
 Author-email: mike_mp@zzzcomputing.com
 License: MIT License
 Location: /.../RSD2018/RSD2018/Server/venv/lib/python3.5/site-packages
 Requires: 
 Required-by: Flask-SQLAlchemy

 # For python3:
 $ pip install mysqlclient
 $ pip show mysqlclient

 Name: mysqlclient
 Version: 1.3.13
 Summary: Python interface to MySQL
 Home-page: https://github.com/PyMySQL/mysqlclient-python
 Author: INADA Naoki
 Author-email: songofacandy@gmail.com
 License: GPL
 Location: /.../RSD2018/RSD2018/Server/venv/lib/python3.5/site-packages
 Requires: 
 Required-by: 
 ```
 - **Install MySQL server:**

 In a new terminal (out of the virtual environment):

 ```sh
 $ sudo apt-get update
 $ sudo apt-get install mysql-server
 ```
 Run secure installation to change some default unsecure settings that come with MySQL:

 ```sh
 $ mysql_secure_installation
 ```

 Check that installation was succesful and MySQL is up and running:

 ```sh
 $ systemctl status mysql.service
 ```

 The output should be:
 
 ```sh
 ● mysql.service - MySQL Community Server
   Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: en
   Active: active (running) since Mon 2018-11-05 11:44:43 CET; 6min ago
  Main PID: 12995 (mysqld)
   CGroup: /system.slice/mysql.service
           └─12995 /usr/sbin/mysqld

 Nov 05 11:44:42 rohan systemd[1]: Starting MySQL Community Server...
 Nov 05 11:44:43 rohan systemd[1]: Started MySQL Community Server.
 ```

Finally, try to run _mysqladmin_, which is a client that lets you run administrative commands and ask for the version of the installation:

```sh
 $ mysqladmin -p -u root version
 Enter password: 

 mysqladmin  Ver 8.42 Distrib 5.7.24, for Linux on x86_64
 Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.

 Oracle is a registered trademark of Oracle Corporation and/or its
 affiliates. Other names may be trademarks of their respective
 owners.

 Server version		5.7.24-0ubuntu0.16.04.1
 Protocol version	10
 Connection		Localhost via UNIX socket
 UNIX socket		/var/run/mysqld/mysqld.sock
 Uptime:			11 min 49 sec

 Threads: 1  Questions: 10  Slow queries: 0  Opens: 115  Flush tables: 1  Open tables: 34  Queries per second avg: 0.014
```

### 1.2. Running the server

  The server must be run inside the virtual environment, so keep a terminal opened with **venv** activated.

 - **Database configuration:**

 To create the _rsd_ user, open a new terminal:

 ```sh
 $ mysql -u root -p
 mysql> create user 'rsd'@'localhost' identified by 'rsd2018';
 mysql> grant all privileges on *.* to 'rsd'@'localhost';
 mysql> create database rsd2018;
 mysql> quit
 ```

 If running on Ubuntu 16.04, open the .sql file and search \& replace the lines that contain `ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;` with `ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;`. Then, add _db\_export.sql_ to user _rsd_ under the name of _rsd2018_ with the command:

 ```sh
 $ mysql -u rsd -p rsd2018 < db_export.sql 
 ```

 - **Running on Flask:**

 From the virual environment:

 ```sh
 $ export FLASK_APP=rsd_2018_app.py
 # Run with Flask:
 $ flask run
 # Run with Python:
 $ Python -m flask run
 # Don't know if there is a difference...
 ```
 
 - **Execution bug:**

 ```sh
 $ . venv/bin/activate
 (venv)$ export FLASK_APP=rsd_2018_app.py 
 (venv)$ python -m flask run

 * Serving Flask app "rsd_2018_app.py"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 Exception in thread Thread-1:
 Traceback (most recent call last):
  File "/usr/lib/python3.5/threading.py", line 914, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.5/threading.py", line 862, in run
    self._target(*self._args, **self._kwargs)
  File "/home/charlie/Workspace/WebProgramming/RSD2018/RSD2018/Server/rsd_2018_app.py", line 24, in run_job
    con = mysql.connect()
  File "/home/charlie/Workspace/WebProgramming/RSD2018/RSD2018/Server/venv/lib/python3.5/site-packages/flaskext/mysql.py", line 39, in connect
    if self.app.config['MYSQL_DATABASE_HOST']:
 AttributeError: 'NoneType' object has no attribute 'config'
 ```

 Might be due to missplacement of some running commands inside the server script? Don't know yet but the server seems to be working.

 ![Screenshot of the server](Server/other/server_1.0.png)


## 2. WorkCell Client.

The REST Client can interact with the server using the following entries and methods:

1. **Logs (POST):**
  
Post a new entry to http://localhost:5000/log. Log entries require the following fields:

 - _cell\_id_: **int type**, number of the WorkCell.
 - _comment_: **string type**, comment attached to the entry.
 - _event_: **string type**, event type, PML\_Idle ...
 - _id_: Maybe ID inside the database? Auto-generated.
 - _time_: time stamp, autogenerated.
 
 ```sh
 $ cd /.../RSD2018/Server/Client/
 $ python POST_example.py

 POST request into RSD server in http://localhost:5000/ 

 The following log was posted: "cell_id: 3, comment: Carlos logs 4.0, event: PML_Held"
 ('Status code: ', 200)
 Log entry was succesfully added. Refresh the browser to see it on the server.
 ```
 ![Screenshot of the server](Server/other/post1.png)

## References

 - Flask [Installation](http://flask.pocoo.org/docs/1.0/installation/#python-version).
 - Flask [Quickstart](http://flask.pocoo.org/docs/1.0/quickstart/).
 - [Flask-MySQL](https://flask-mysql.readthedocs.io/en/latest/) extension.
 - Creating a WebApp from scratch using Python Flask and MySQL [tutorial](https://code.tutsplus.com/es/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972).