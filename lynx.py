#
# date: 22.05.2020
# author: Zerb3ru5
# description: A simple cli programme to hide and lock folders
#

import click
import os
from locker import Locker


lr = Locker()


@click.group()
def main():
    pass


@main.command()
@click.argument('dir')
@click.option('--password', '-pw', prompt='Set a password for unlocking', required=True)
def hide(dir, password):
    lr.hide(dir, password)


@main.command()
@click.argument('dir')
def reveal(dir):
    password = click.prompt('Please enter your password to unlock')
    lr.reveal(dir, password)


if __name__ == "__main__":
    main()
