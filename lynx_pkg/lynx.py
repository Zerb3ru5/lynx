#
# date: 22.05.2020
# author: Zerb3ru5
# description: A simple cli programme to hide and lock folders
#

import click
import os
import json
from lynx_pkg.locker import Locker


lr = Locker()
feedback_codes = dict()


@click.group()
def main():

    # load all the possile feedbacks
    with open('C:\\Users\\Nutzer\\AppData\\Local\\lynx\\feedback_codes.json', 'r') as file:
        global feedback_codes
        feedback_codes = json.load(file)


# access the hide function of the locker
@main.command()
@click.argument('dir')
def hide(dir):

    # check if the directory is valid
    response = lr.isValidDirectory(dir)
    feedback(response)

    if response == 900:

        # ask for the password if the path isn't known or the user wants a new one and access the hide function
        if not lr.isKnownPath(dir):
            password = click.prompt(
                'Please enter your password to lock this folder')
        elif click.confirm('You already saved a password for this directory. Do you want to create a new one?'):
            password = click.prompt(
                'Please enter your new password to lock this folder')
        else:
            password = lr.getPassword(dir)

        response = lr.hide(dir, password)
        feedback(response)


# access the reveal function of the locker
@main.command()
@click.argument('dir')
def reveal(dir):

    # ask for the password and access the reveal function
    password = click.prompt('Please enter your password to unlock')
    response = lr.reveal(dir, password)
    feedback(response)


def feedback(code):
    message = feedback_codes[f'{code}']
    click.secho('\n' + message[0] + '\n' + message[1] + '\n', fg=message[2])


if __name__ == "__main__":
    main()
