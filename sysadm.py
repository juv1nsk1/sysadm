import sys
from _lib import *

DEBUG=True

if __name__ == "__main__":

    body = ""

    if len(sys.argv) >= 2 and sys.argv[1] == 'ids': 
        body += check_file_changes()
        body += check_ssh_connections()
        body += is_process_running()
        body += check_site_available()
        body += check_cpu_usage()
        body += check_ram_usage()
        body += check_io_usage()
        subject = "Defcon protocol"
    else:    
        body += check_backup()
        body += check_disk_usage()
        body += check_wordpress_core_update()
        subject = "Cocon protocol"

    if body:
        if DEBUG: print(body)
        else: 
            send_email(subject, body, to_email)
            
