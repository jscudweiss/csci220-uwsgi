# Python WSGI Example

A starter project for Clark's Databases course (CSCI 220). This project includes a web server and database.

Follow these steps to get started:

## Step 0: Clone This Repository

Unless otherwise specified, all commands mentioned below should be run within the root directory of this repository.

## Step 1: Install Docker

This project includes several components: 

- uWSGI, which will run your Python code
- NGINX, a web server which will allow browsers to communicate with uWSGI
- PostgresSQL, a database which will store your application's persistent data

It could be time-consuming to install and configure all of these on your computer, but thankfully there is a better way: Docker! Install Docker, and it will be easy to run all of these components.

## Step 2: Configure Database Password

It is a bad idea to run software with default passwords. To configure the password for the database, you will need to write them in a `.env` file. Follow these steps:

1. Copy `dot_env_example` to `.env`
2. Run `chmod 600 .env` to prevent other users from reading your `.env` file
3. Edit `.env`, changing the text `RANDOM_PASSWORD` to a password which is actually random

## Step 3: Start the Docker Services

Run:
```
docker-compose up -d
```

The first time you run it, this command will take a few minutes to complete. This is because Docker needs to download the code for PostgresSQL, etc.

## Step 4: Load the Application

Load <http://localhost> and you should see "Hello World".
