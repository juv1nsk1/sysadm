### How to Install Munin on a Single Machine (Server and Plugins with Nginx Authentication)

Munin is a powerful system monitoring tool that allows you to track various metrics of your server, including disk, memory, and CPU usage. This guide will walk you through installing Munin on a single machine, setting up the Munin server, enabling important plugins (disk, memory, and CPU), and configuring Nginx with basic authentication to secure the Munin web interface.

---

#### Step 1: Update Your System

Before installing any software, it's a good idea to update your package list:

```bash
sudo apt update
sudo apt upgrade
```

#### Step 2: Install Munin and Required Packages

To install Munin and Nginx, run the following command:

```bash
sudo apt install munin munin-node nginx apache2-utils
```

This installs:
- `munin`: the Munin server
- `munin-node`: the Munin node (agent) to monitor the local machine
- `nginx`: the web server to host Munin's web interface
- `apache2-utils`: to generate a password for securing the web interface

#### Step 3: Configure Munin

By default, Munin stores configuration files in `/etc/munin/`. You will need to edit the main configuration file to define the monitored node (the machine itself).

1. Open the Munin configuration file:

   ```bash
   sudo vim /etc/munin/munin.conf
   ```

2. Look for the section where you define the hostname and modify it like this:

   ```
   [localhost]
     address 127.0.0.1
     use_node_name yes
   ```

This tells Munin to monitor the local machine.

#### Step 4: Enable Plugins for Disk, Memory, and CPU

Munin uses plugins to collect various metrics. By default, Munin enables some plugins automatically, but you can manually enable more as needed.

1. List available plugins:

   ```bash
   sudo munin-node-configure --suggest
   ```

2. Enable specific plugins (disk, memory, and CPU) by creating symlinks to the `/etc/munin/plugins/` directory:

   ```bash
   sudo ln -s /usr/share/munin/plugins/diskstats /etc/munin/plugins/diskstats
   sudo ln -s /usr/share/munin/plugins/memory /etc/munin/plugins/memory
   sudo ln -s /usr/share/munin/plugins/cpu /etc/munin/plugins/cpu
   sudo ln -s /usr/share/munin/plugins/contextswitch /etc/munin/plugins/contextswitch
   sudo ln -s /usr/share/munin/plugins/uwsgi_status /etc/munin/plugins/uwsgi_status
   sudo ln -s /usr/share/munin/plugins/nginx_status /etc/munin/plugins/nginx_status
   sudo ln -s /usr/share/munin/plugins/postgres_bgwriter /etc/munin/plugins/postgres_bgwriter
   sudo ln -s /usr/share/munin/plugins/postgres_connections /etc/munin/plugins/postgres_connections
   sudo ln -s /usr/share/munin/plugins/postgres_cache /etc/munin/plugins/postgres_cache
   sudo ln -s /usr/share/munin/plugins/postgres_locks /etc/munin/plugins/postgres_locks
   sudo ln -s /usr/share/munin/plugins/postgres_querylength /etc/munin/plugins/postgres_querylength
   sudo ln -s /usr/share/munin/plugins/postgres_size_ /etc/munin/plugins/postgres_size_
   ```

3. Restart the Munin node service to apply the changes:

   ```bash
   sudo systemctl restart munin-node
   ```

4. Check if the plugins are working:

   ```bash
   telnet localhost 4949
   ```

   After connecting, type `list` to see active plugins and `fetch plugin_name` to see the plugin's output.

#### Step 5: Configure Nginx for Munin

1. First, create a Munin configuration file for Nginx:

   ```bash
   sudo vim /etc/nginx/sites-available/munin
   ```

2. Add the following content to the file:

   ```nginx
   server {
       listen 80;
       server_name localhost;

       location /munin {
           auth_basic "Restricted Access";
           auth_basic_user_file /etc/nginx/.htpasswd;
           alias /var/cache/munin/www;
           index index.html;
       }
   }
   ```

3. Enable the site by creating a symlink:

   ```bash
   sudo ln -s /etc/nginx/sites-available/munin /etc/nginx/sites-enabled/
   ```

4. Reload Nginx to apply the changes:

   ```bash
   sudo systemctl reload nginx
   ```

#### Step 6: Set Up Basic Authentication

To secure the Munin web interface, you can use basic authentication with a username and password.

1. Create a username and password for Munin access:

   ```bash
   sudo htpasswd -c /etc/nginx/.htpasswd username
   ```

   Replace `username` with your desired username. You will be prompted to create a password.

2. Restart Nginx:

   ```bash
   sudo systemctl restart nginx
   ```

#### Step 7: Access Munin Web Interface

Now, you can access the Munin web interface by navigating to `http://your-server-ip/munin`. You will be prompted for a username and password before viewing the Munin dashboard.

---

### Summary

- **Munin Installation:** `sudo apt install munin munin-node`
- **Nginx Setup:** Created a server block for `/munin` and enabled basic authentication.
- **Plugins Enabled:** Disk, memory, and CPU monitoring.
- **Access:** `http://your-server-ip/munin` with the username and password created during basic authentication setup.

With Munin and Nginx running, you now have a monitoring of iowait, contextswitch, memory usage and main database status.

Author: @juv1nsk1
