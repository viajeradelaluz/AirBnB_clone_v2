#!/usr/bin/python3
"""
Module (based on the file 1-pack_web_static.py) that distributes an archive to
your web servers, using the function do_deploy:
    - Prototype: def do_deploy(archive_path):
    - Returns False if the file at the path archive_path doesn't exist
    - The script should take the following steps:
        - Upload the archive to the /tmp/ directory of the web server
        - Uncompress the archive to the folder:
          /data/web_static/releases/<archive filename without extension>
        - Delete the archive from the web server
        - Delete the symbolic link /data/web_static/current from the web server
        - Create a new the symbolic link /data/web_static/current on the web
          server, linked to the new version of your code
        (/data/web_static/releases/<archive filename without extension>)
    - All remote commands must be executed on your both web servers
      (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
    - Returns True if evething is OK, otherwise returns False
    - You must use this script to deploy it on your servers:
      xx-web-01 and xx-web-02
"""

from fabric.api import run, put, env
from os.path import exists

env.hosts = ['52.201.246.143', '18.234.216.100']


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    Returns False if the file at the path archive_path doesn't exist
    """
    if exists(archive_path) is False:
        return False
    try:
        filename = archive_path.split("/")[-1]
        unfile = filename.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("mkdir -p {}{}".format(path, unfile))
        run("tar -xzf /tmp/{} -C {}{}".format(filename, path, unfile))
        run("rm -rf /tmp/{}".format(filename))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, unfile))
        run('rm -rf {}{}/web_static'.format(path, unfile))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, unfile))
        return True
    except Exception:
        return False
