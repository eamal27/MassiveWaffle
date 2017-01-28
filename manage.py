#!env/bin/python3

from flask_script import Manager
from server import app

manager = Manager(app)

if __name__ == "__main__":
    manager.run()
