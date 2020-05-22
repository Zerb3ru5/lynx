# 
# date: 22.05.2020
# author: Zerb3ru5
# description: A simple cli programme to hide and lock folders
#

import click
import os

@click.group()
def main():
    pass

@main.command()
@click.argument('directory')
def keep(directory):
    cmd = 'attrib +h %s'%directory
    click.echo(cmd)
    os.system(cmd)

if __name__ == "__main__":
    main()