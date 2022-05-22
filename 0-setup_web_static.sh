#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static.

# Install Nginx if it not already installed
if [ ! -x /usr/sbin/nginx ]; then
    sudo apt update -y
    sudo apt install --allow-downgrades nginx -y
    sudo ufw allow 'Nginx HTTP'
fi

# Create these folders if they don't already exist:
#   /data/web_static/shared/            /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared /data/web_static/releases/test

# Create a fake HTML file /data/web_static/releases/test/index.html
#   (with simple content, to test your Nginx configuration)
echo 'Holberton School' | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder.
#   If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group recursively
sudo chown -hR ubuntu:ubuntu /data/

# - Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static.
#    - Use alias inside your Nginx configuration
sudo sed -i '27i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
sudo service nginx restart
