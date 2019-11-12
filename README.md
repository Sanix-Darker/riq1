<img src="./images/logo.png"/>

# Riq1

Change your ip address for each request you make ! Simple, Smart, Clear !

**NB: This program is for learning only, am not responsible of the bad use of it !**


## Requirements

- python (3.x is recommended)


## How to install

You just have to run:

```shell
# We install requirements
pip install -r requirements.txt
```

## How it works

When the main script it launched,
it check first the ip_list if the file is too old (here i configured 100s, you can change it later in ./app/settings.py), if it's need to fetch news ip proxy then it will scrap them online,
So after that the script use the session of the concerned ip proxy to emit te request.


## How to use it

To use it you just have to run main.py and follow instructions
Just hit:

```shell
# We clone the project
git clone https://github.com/Sanix-Darker/riq1.git

# We browse to the project
cd path/to/the/project

# Then we browse to ./app/
cd app
python main.py
```

## Demo

<img src="./images/demo.gif"/>


## MIT LICENSE

## Author

- Sanix-darker