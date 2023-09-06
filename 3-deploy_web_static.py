#!/usr/bin/python3
"""Create and distributes an archive to web servers"""
import os.path
import time
from fabric.api import local
from fabric.operations import env, put, run

env.hosts = ['35.174.208.45', '54.165.221.49']
env.user = 'ubuntu'
env.key_filename = '/home/ubuntu/.ssh/id_rsa'

def do_pack():
    """Generate a .tgz archive from web_static folder"""
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static/".format(
            time.strftime("%Y%m%d%H%M%S")))
        return "versions/web_static_{}.tgz".format(
            time.strftime("%Y%m%d%H%M%S"))
    except Exception:
        return None

def do_deploy(archive_path):
    """Distribute an archive to web servers"""
    if not os.path.isfile(archive_path):
        return False

    try:
        file_name = os.path.basename(archive_path)
        file_name_no_ext = os.path.splitext(file_name)[0]
        remote_path = "/data/web_static/releases/{}".format(file_name_no_ext)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(remote_path))
        run("tar -xzf /tmp/{} -C {}/".format(file_name, remote_path))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}/".format(remote_path, remote_path))
        run("rm -rf {}/web_static".format(remote_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(remote_path))

        print("Deployment done")
        return True
    except Exception:
        return False

def deploy():
    """Create and distributes an archive to web servers"""
    try:
        archive_path = do_pack()
        return do_deploy(archive_path)
    except Exception:
        return False
