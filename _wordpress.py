import mysql.connector
from datetime import datetime, timedelta

host = "localhost"  
user = "username"   
password = "password" 
database = "mysql"  

def get_recent_plugin_changes(host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        cutoff_time = datetime.now() - timedelta(minutes=5)
        query = "SELECT PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_STATUS, PLUGIN_LIBRARY FROM mysql.plugin WHERE INSTALL_TIME >= %s OR MODIFY_TIME >= %s"
        cursor.execute(query, (cutoff_time, cutoff_time))

        plugin_changes = cursor.fetchall()

        cursor.close()
        conn.close()

        return plugin_changes
    except Exception as e:
        print("Error:", e)
        return []

def check_plugins():


    recent_plugin_changes = get_recent_plugin_changes(host, user, password, database)

    if recent_plugin_changes:
        print("Recent MySQL Plugin Changes (added or modified) in the last 5 minutes:")
        for plugin_change in recent_plugin_changes:
            plugin_name, plugin_version, plugin_status, plugin_library = plugin_change
            print(f"Plugin: {plugin_name}, Version: {plugin_version}, Status: {plugin_status}, Library: {plugin_library}")
    else:
        print("No recent MySQL plugin changes found.")


def get_recent_user_changes(host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        cutoff_time = datetime.now() - timedelta(minutes=5)
        query = "SELECT user_login, user_registered, user_modified FROM wp_users WHERE user_registered >= %s OR user_modified >= %s"
        cursor.execute(query, (cutoff_time, cutoff_time))

        user_changes = cursor.fetchall()

        cursor.close()
        conn.close()

        return user_changes
    except Exception as e:
        print("Error:", e)
        return []

def check_user():

    recent_user_changes = get_recent_user_changes(host, user, password, database)

    if recent_user_changes:
        print("Recent WordPress User Changes (added or modified) in the last 5 minutes:")
        for user_change in recent_user_changes:
            user_login, user_registered, user_modified = user_change
            print(f"User: {user_login}, Registered: {user_registered}, Modified: {user_modified}")
    else:
        print("No recent WordPress user changes found.")


