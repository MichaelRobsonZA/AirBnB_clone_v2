#!/usr/bin/python3
"""
This Fabric script generates a compressed archive (.tgz)
from the contents of the web_static folder in your AirBnB Clone.
"""

from fabric.api import *
from datetime import datetime

def do_pack():
    """
    Creates a compressed archive of web_static content.

    Returns:
        str: The path to the generated archive if successful,
             None if the archive creation fails.
    """
    try:
        local("mkdir -p versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(date)
        compression_result = local("tar -cvzf {} web_static".format(archive_path))
        return archive_path if compression_result.succeeded else None
    except Exception:
        return None
