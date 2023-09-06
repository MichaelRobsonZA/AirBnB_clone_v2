#!/usr/bin/env bash
# set up the NGINX config for web_static
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install nginx
# make file structure
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
# Create a fake HTML file
echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html
# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
# Create owner and permissions
sudo chown -hR ubuntu:ubuntu /data/
# Update nginx configuration content
conf="\\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}"
sudo sed -i "45i $conf" /etc/nginx/sites-available/default
sudo service nginx start
sudo service nginx restart
sudo service nginx reload
