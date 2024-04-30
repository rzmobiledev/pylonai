
# PylonAI 

Backend Developer Technical Test at Pylon.AI Pte Ltd

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)![MicrosoftSQLServer](https://img.shields.io/badge/Microsoft%20SQL%20Server-CC2927?style=for-the-badge&logo=microsoft%20sql%20server&logoColor=white)![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)  

This project is developed with python Flask, Postgresql and MicrosoftSQLServer as external database. prerequisites :

* **Python:** Please install python in your machine. Minimum requirements is Python version 3.10.5. This project uses 3.10.5 version
* **Docker:** Install Docker and docker compose.
* **Learn Once, Write Anywhere:** We don't make assumptions about the rest of your technology stack, so you can develop new features in React without rewriting existing code. React can also render on the server using Node and power mobile apps using [React Native](https://reactnative.dev/).

[Learn how to use the API endpoint of this project](https://react.dev/learn).

## Installation
* **pyenv**. Pyenv lets you easily switch between multiple versions of Python. It's simple, unobtrusive, and follows the UNIX tradition of single-purpose tools that do one thing well. [Installation instruction](https://github.com/pyenv/pyenv)
* **python** with pyenv already setup, kindly type 
    ```bash
    pyenv install 3.10.5
    ```
    wait till installation process completed.
* **Project Code**. Download Project code to your folder
    ```bash
    git clone https://github.com/rzmobiledev/pylonai.git
    ```
* **Activate python environment**.
    `cd` to project directory and activate python version inside project folder
    ```bash
    pyenv local 3.10.5
    ```
    now this project folder has python version `3.10.5`. Simply check it
    ```bash
    python -V
    ```
    ![Logo](https://i.ibb.co/D8vyBps/python-version.png)

    Next activate local `python environment`. Please note this command only valid for linux or mac os. Kindly refer to google how to activate this with Windows.
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
    ![Logo](https://i.ibb.co/K6ZckQ4/python-activation.png)
* **Install dependencies**. Type this command in your terminal.
    ```bash
    pip install -r requirements.txt
    ```
    and wait for installation process to finish.

## Problem with ODBC Driver
If you find error on installation process, please check all required dependencies for your machine to run this project smooth. Since i use *Debian 12 WSL* i found some good drivers for my machine. [Check this link](https://docs.google.com/document/d/13IYcC1A28eQOiOX70V_85JMni0OvVF0CY_CqXBlkWRE/edit)


## Install Postgres
Make sure you docker is installed. You are going to use postgres docker container.
* **Setup postgres**. Open your docker desktop or docker cli, and run :
    ```bash
    docker run -p 5432:5432 -d --name pylondb -e POSTGRES_DB=pylon -e POSTGRES_USER=pylon -e POSTGRES_PASSWORD=pylon postgres:16.1
    ```
    always make sure that your postgres docker container is running.
    ```bash
    docker ps
    ```
    ![logo](https://i.ibb.co/9pNyGhz/docker-ps.png)
    now your postgres is done and completed. You might want to use postgres client such as `pgAdmin` to interact with your database as you have ported it to local port 5432.

## Run project
* **activate python**. Make sure your python is activated within the project folder as previous step.
* **ENV File**. In project root folder, create `.env` file. You need to put some variables here for your application to run. 
```bash
FLASK_APP=app
DEBUG=True
PGDATABASE_URL=postgresql://pylon:pylon@127.0.0.1:5432/pylon
PYLONSERVER=[your SQL server name]
PYLONDATABASE=[your SQL SERVER DB name]
PYLONUSERNAME=[your SQl SERVER username]
PYLONPASSWORD=[Your SQL SERVER password]
JWT_SECRET_KEY=x&9^%pyl0nx@#!0)9ZAE8
```
* **Run unit test**. Please run the unit test to check everything okay and run smoothly. If any failed, please the log and report back to me. But as long as you have a connection with **SampleManpowerList** database, it shoud be no problem.
    ```bash
    pytest -s
    ```
    ![Logo](https://i.ibb.co/BPWS7Rf/unit-test.png)

* **Run application**. Now as unit test run perfectly, next is to launch your app.
    ```bash
    flask --app app run
    ```
    ![Logo](https://i.ibb.co/LShV64W/flask-run.png)

    Your app is online now.
    Please open your browser and type `http://127.0.0.1:5000/api/v1` and hit enter.


## Dockerizing App
If above setup and installation process not work for you, you might want to run the app within docker container.

**Note**. *With docker container, employee endpoints is unaccessible due to limitation with external host as employee db beyond docker container*.

* **Change `.env` file**. Kindly open your `.env` file and change `PGDATABASE_URL` with this variable value.
    ```bash
    PGDATABASE_URL=postgresql://pylon:pylon@db:5432/pylon
    ```
    Do not forget to revert back with prev value if you run on local.
* **Docker compose**. open terminal within the project.
    ```bash
    docker compose build
    ```
    and
    ```bash
    docker compose up
    ```
    then in your browser open `http://127.0.0.1:3000/api/v1/`