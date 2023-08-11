# contact juvinski@gmail.com
import os
import re
import time
import tarfile
import smtplib
import subprocess
import requests
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from _config import *


def get_partition_usage():
    skiplist=['devfs','cdrom']    
    output = subprocess.check_output(["df", "-h"]).decode("utf-8")
    lines = output.strip().split("\n")[1:] 

    partition_data = []
    for line in lines:        
        parts = line.split()
        if '%' in parts[4] and parts[0] not in skiplist: 
            partition = {
                "filesystem": parts[0],
                "size": parts[1],
                "used": parts[2],
                "available": parts[3],
                "percent_used": int(parts[4][:-1])  
            }
            partition_data.append(partition)
    return partition_data



def check_disk_usage():
    partitions = get_partition_usage()
    problematic_partitions = [partition for partition in partitions if partition["percent_used"] > disk_space_threshold]
    output=[]
    if problematic_partitions:        
        for partition in problematic_partitions:
             output.append("Disk: {} using: {}%".format(partition["filesystem"], partition["percent_used"]))
    return "\n".join(output)

def get_recently_modified_conf_files(root_dir, time_threshold):
    recently_modified_files = []
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if (file.endswith(".conf") or file.endswith(".sh") or file.endswith(".cnf") or file in sensitive_files_change) and file not in  ignore_files_change:                 
                
                try:
                    file_path = os.path.join(root, file)
                    modified_time = os.path.getmtime(file_path)
                    current_time = time.time()
                    time_diff = current_time - modified_time                    
                    if time_diff <= time_threshold:                        
                        utc_datetime = datetime.utcfromtimestamp(modified_time)                        
                        time_difference = timedelta(hours=-3) 
                        br_datetime = utc_datetime + time_difference
                        formatted_br_datetime = br_datetime.strftime('%Y-%m-%d %H:%M:%S')                          
                        recently_modified_files.append("File {} changed on {}.\n".format(file_path, str(formatted_br_datetime)))
                except:
                    error=file    
    return recently_modified_files

def check_file_changes():
    output=[]
    for root_directory in folder_change:
        time_threshold = etc_hours_change * 60 * 60  
        recently_modified_conf_files = get_recently_modified_conf_files(root_directory, time_threshold)
        
        if recently_modified_conf_files:
            for file_path in recently_modified_conf_files:
                output.append(file_path)
       
    return "\n".join(output)

def get_recent_remote_access_info(log_file, time_threshold):
    current_time = datetime.now()
    cutoff_time = current_time - timedelta(seconds=time_threshold)
    access_info = []
    
    with open(log_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            match = re.search(r'Accepted.* for ([a-zA-Z0-9_-]+) from ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', line)
            if match:
                line=line.replace('  ',' ')
                day=line.split(' ')[1]
                
                hour=line.split(' ')[2]
                current_month = current_time.strftime('%m')
                timestamp_str=f'{current_time.year} {current_month} {day} {hour}'
                
                try:
                    timestamp = datetime.strptime(timestamp_str, '%Y %m %d %H:%M:%S')
                except:                    
                    print("Invalid data format on {}!".format(log_file))

                if timestamp >= cutoff_time:
                    username = match.group(1)
                    ip = match.group(2)
                    access_info.append({
                        "username": username,
                        "ip": ip,
                        "timestamp": timestamp
                    })
    
    return access_info

def check_ssh_connections():
    log_file = "/var/log/auth.log"  
    time_threshold = ssh_time_threshold  * 3600 
    output=[]

    if os.path.exists(log_file):
        recent_remote_access_info = get_recent_remote_access_info(log_file, time_threshold)        
        if recent_remote_access_info:            
            for info in recent_remote_access_info:
                username = info["username"]
                ip = info["ip"]
                if ip not in knowed_ssh_host:
                    timestamp = info["timestamp"]                
                    output.append("User {} via IP {} on {} through {} \n".format(username, ip, timestamp, get_whois_details(ip)))
    else:        
        output.append("SSH log file not found. {}" .format(log_file))
    return "\n".join(output)

def get_whois_details(ip_address):    
    try:                
        cmd = ["whois", ip_address]
        result = subprocess.run(cmd, capture_output=True, text=True)         
        result =  re.search(r"owner:\s+([\w\s.]+)", result.stdout, re.IGNORECASE)
        return result.group(1)
    except subprocess.CalledProcessError:
        return None


def check_tgz_file(file_path):
    try:
        with tarfile.open(file_path, "r:gz") as tar:
            #tar.list()  
            return True
    except tarfile.ReadError:
        return False     
    return False

def check_backup():    
    output=[]
    for backup_file in backup_files:
        if os.path.exists(backup_file):           
            if backup_file.endswith('.tgz'):
                if check_tgz_file(backup_file) == False:
                    output.append("Backup {} corrupted.\n".format(backup_file))
        else:
            output.append("Backup {} not found.\n".format(backup_file))
    return "\n".join(output)

def is_process_running():
    output=[]
    for process in process_list:
        try:
            subprocess.check_output(["systemctl", "is-active", "--quiet", process])
        except subprocess.CalledProcessError:
            output.append("The {} process is not running.\n".format(process))
    return "\n".join(output)

def send_email(subject="Server report", body='', to_email=''):    
    msg = MIMEMultipart()
    msg['From'] = smtp_from
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() 
        server.login(smtp_user, smtp_k)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()        
    except Exception as e:
        print("Error sending email:", e)


def find_wordpress_version():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

        # Fetch the HTML of the WordPress homepage with headers
        response = requests.get(wp_site_url, headers=headers)
        html = response.text
        
        generator_pattern = r'<meta\s+name="generator"\s+content="WordPress\s+([\d.]+)"'
        match = re.search(generator_pattern, html)        

        if match:
            wordpress_version = match.group(1)        
            return  match.group(1)
        
    except Exception as e:
        print("Error:", e)
    return ''

def get_latest_wordpress_version():
    try:
        url = "https://wordpress.org/download/"
        response = requests.get(url)
        html = response.text
        
        version_pattern = r'Download WordPress ([\d.]+)'
        match = re.search(version_pattern, html)

        if match:
            latest_version = match.group(1)            
            return latest_version
        
    except Exception as e:
        print("Error:", e)

def check_wordpress_core_update():
    version = find_wordpress_version()
    last_version=get_latest_wordpress_version()
    if version != last_version:
        return "Your server is running Wordpress {} but there is a newest version {} available.\n".format(version, last_version)
    else:
        return ''


def check_site_response(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

        start_time = time.time()
        response = requests.get(url, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        status_code = response.status_code

        return status_code, response_time
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}. Site {url} is not responsive.")


def check_site_available():
    output=[]
    for site in check_sites:
        status_code, response_time = check_site_response(site)
        if status_code != 200:
            output.append(f"{site} is not avaialbe. Error {status_code}")
        elif response_time > site_timeout_threshold:
            output.append(f"{site} exceeds threshold. Current {response_time:.2f} seconds\n")
    return "\n".join(output)
