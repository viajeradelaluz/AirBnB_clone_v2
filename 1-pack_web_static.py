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
from fabric.api import local
from os import path


def do_pack():
    """ Generates a .tgz archive from web_static folder """
    try:
        if not path.exists("versions"):
            local('mkdir versions')
        time = datetime.now()
        format = "%Y%m%d%H%M%S"
        file = 'versions/web_static_{}.tgz'.format(time.strftime(format))
        local('tar -cvzf {} web_static'.format(file))
        return file
    except Exception:
        return None
