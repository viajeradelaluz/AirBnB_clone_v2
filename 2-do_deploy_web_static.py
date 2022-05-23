#!/usr/bin/python3
"""
Module (based on the file 1-pack_web_static.py) that distributes an archive to your web servers, using the function do_deploy:
    Prototype: def do_deploy(archive_path):
    Returns False if the file at the path archive_path doesn't exist
    The script should take the following steps:
        Upload the archive to the /tmp/ directory of the web server
        Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension> on the web server
        Delete the archive from the web server
        Delete the symbolic link /data/web_static/current from the web server
        Create a new the symbolic link /data/web_static/current on the web server, linked to the new version of your code (/data/web_static/releases/<archive filename without extension>)
    All remote commands must be executed on your both web servers (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
    Returns True if all operations have been done correctly, otherwise returns False
    You must use this script to deploy it on your servers: xx-web-01 and xx-web-02
"""

from fabric.api import run, put, env
from os.path import exists
from sys import argv

env.hosts = ['52.201.246.143', '18.234.216.100']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """  """
    try:
        if exists(archive_path) is False:
            raise Exception

        file = argv[3].split('/')[1]
        unfile = file.split('.')[0]
        releases = '/data/web_static/releases/'
        current = '/data/web_static/current'

        put('archive_path', '/tmp/')
        run('mkdir -p {}{}'.format(releases, unfile))
        run('tar -xzf /tmp/{} -C {}'.format(file, releases))
        run('rm -rf /tmp/{}'.format(file))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(releases, unfile))
        run('rm -rf {}{}/web_static'.format(releases, unfile))
        run('rm -rf {}'.format(current))
        run('ln -s {}{} {}'.format(releases, unfile, current))

        return True

    except Exception:
        return False
