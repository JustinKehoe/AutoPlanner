import dill
from os import path
from api import caller, setup

if __name__ == '__main__':
    if path.exists("session.pkl"):
        dill.load_module("session.pkl")

    print("DONE")

    # Save session for persistence
    # dill.dump_module('session.pkl')
