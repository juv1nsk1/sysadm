from datetime import datetime

ids_interval=1 #hour

backup_files =[ "/srv/storage/dump.tgz"]
              
folder_change = ['/etc','/tmp']
process_list=['ssh','nginx']
knowed_ssh_host=['177.92.48.240']

wp_site_url = "" 
check_sites = ["https://google.com.br", "https://twitter.com"]


disk_space_threshold = 90 
etc_hours_change=ids_interval
ssh_time_threshold = ids_interval
site_timeout_threshold = 1
sensitive_files_change=['passwd','hosts','crontab']
ignore_files_change=['subscriptions.conf']

to_email = "juvinski@gmail.com"
smtp_server="mail.smtp2go.com"
smtp_port="587"
smtp_user="j@gmail.com.br"
smtp_from="Server <server@gmail.com.br"
smtp_k="PASSWORD"
