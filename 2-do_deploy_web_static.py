#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env, put, run

# Define your server information
env.hosts = ['35.174.208.45', '54.165.221.49']

def do_deploy(archive_path):
    """
    Distributes an archive to the web server.

    Args:
        archive_path (str): The path of the archive to distribute.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    name = file_name.split(".")[0]

    # Upload the archive to the /tmp/ directory on the server
    if put(archive_path, "/tmp/{}".format(file_name)).failed:
        return False

    # Create the necessary directory structure
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False

    # Extract the archive
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file_name, name)).failed:
        return False

    # Clean up temporary files
    if run("rm /tmp/{}".format(file_name)).failed:
        return False

    # Move files to the correct location
    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed:
        return False

    # Clean up unnecessary directories
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False

    # Create a symbolic link to the new release
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed:
        return False

    return True
