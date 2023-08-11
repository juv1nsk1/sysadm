from datetime import datetime

ids_interval=1 #hour

backup_files =[ "/srv/storage/dump.tgz","/tmp/a.tgz"]
              
folder_change = ['/etc','/tmp']
process_list=['ssh','nginx', 'mariadb']
knowed_ssh_host=['171.92.48.240']
trusted_ssh_isp=['Ligga Telecomunica']

wp_site_url = "https://www2.site.com/" 
check_sites = ["https://google.com.br", "https://twitter.com", wp_site_url]


disk_space_threshold = 90 
cpu_threshold = 90
ram_threshold = 90 
io_threshold_bytes_per_sec= 49012254720
etc_hours_change=ids_interval
ssh_time_threshold = ids_interval
site_timeout_threshold = 1
sensitive_files_change=['passwd','hosts','crontab']
ignore_files_change=['subscriptions.conf']

to_email = "none@gmail.com"
smtp_server="mail.smtp2go.com"
smtp_port="587"
smtp_user="j@gmail.com.br"
smtp_from="Server <server@gmail.com.br"
smtp_k="PASSWORD"


