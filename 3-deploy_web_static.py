#!/usr/bin/python3
"""
Module that generates a .tgz archive from the contents of the web_static
folder, using the function do_pack.
    - Prototype: def do_pack():
    - All files in the folder web_static must be added to the final archive
    - All archives must be stored in the folder versions (your function should
      create this folder if it doesn't exist)
    - The name of the archive created must be
      web_static_<year><month><day><hour><minute><second>.tgz
    - The function do_pack must return the archive path if the archive has
      been correctly generated. Otherwise, it should return None
"""

from datetime import datetime
from fabric.api import env, local, put, run
from os.path import exists


def do_pack():
    """ Generates a .tgz archive from web_static folder """
    try:
        if not exists("versions"):
            local('mkdir versions')
        time = datetime.now()
        format = "%Y%m%d%H%M%S"
        file = 'versions/web_static_{}.tgz'.format(time.strftime(format))
        local('tar -cvzf {} web_static'.format(file))
        return file
    except Exception:
        return None


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


def deploy():
    """
    Call do_pack and do_deploy
    """
    try:
        archive_path = do_pack()
    except Exception:
        return False

    return do_deploy(archive_path)
