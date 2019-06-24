## **WatchDog**

### **BackEnd Repo**

To start with this repo, run the following command to build the repo
```bash
docker-compose up --build -d
```

Wait a while for it to pull every necessary files. After installation, confirm the containers has been created and running
```bash
docker container ls
```

You should see your container. If you don't see it, run the following
```bash
docker container start watchdog
```

Login to the interactive shell in order to view logs and run the application in interactive mode
```bash
docker exec -ti watchdog bash
```

To run the app in interactive mode, run command in bash
```bash
./app.py
```

On your local computer, create a ***Python 3.6*** virtual environment and run the following
```
pip install --editable .
```

AND

```
hooks4git --init
```

This installs the packages to use in your virtual environment for Intellisense and at the same time setup Git Hooks

#### CLI COMMANDS
A CLI tool called `pavshell` has been created inside the repo and can be used for minor commands

* To create a controller
```bash
pavshell create:controller controller_name
```

* To create a model file
```bash
pavshell create:model model_name
```

SQLAlchemy model classes are to be defined in `models/` package. Here you define any SQLAlchemy mappings

Logic, computations e.t.c are to go into the `controllers/` package

in the `route/views.py` file, define your routes (Flask style) and perform any computation that deals with request objects