import sqlite3
import secrets
import datetime
import userattack
conn = sqlite3.connect('db.sql', check_same_thread=False)
cursor = conn.cursor()



def initdb():
    try:
        cursor.execute("DROP TABLE users;")
        print("DROPPING TABLE....")
    except:
        pass
    print("CREATING NEW TABLE...")
    cursor.execute("CREATE TABLE users ("
                    "apikey text,"      # api key -> string
                    "maxtime integer,"  # max time -> int
                    "cooldown integer," # cooldown -> int
                    "expiry text,"      # expiry -> string formatted mm/dd/yyyy
                    "whitelist text,"   # whitelisted ip -> string
                    "concurrents integer," #concurrents -> int
                    "vip integer)") #vip -> int 1 = vip,0=novip
    conn.commit()
    print("TABLE HAS BEEN RESET")

def adduser(maxtime, cooldown,days,concurrents,vip):
    apikey = secrets.token_urlsafe(16)
    enddate = (datetime.datetime.now() + datetime.timedelta(days=int(days))).strftime('%m/%d/%Y')
    cursor.execute(f"INSERT INTO users VALUES ('{apikey}', {maxtime},{cooldown},'{enddate}','undefined',{concurrents},{vip})")
    conn.commit()
    userattack.User(key=apikey, maxtime=maxtime, conncurrents=concurrents, cooldown=cooldown, expiry=enddate,isvip=(vip > 0))
    print(f"Added user: \nKey: {apikey}\nExpires: {enddate}\nCooldown: {cooldown}\nConcurrents: {concurrents}\nMaxtime: {maxtime}\nVip: {vip}")

if __name__ == '__main__':
    s = input(" Enter 1 to reset the db\n2 to add a user\n3 to change whitelisted IP\n: ")
    if s == '1':
        initdb()
    elif s == '2':
        newtime = int(input("Enter max time: "))
        newcooldown = int(input("Enter cooldown time: " ))
        newdays = int(input("Enter amount of days until expiry: "))
        newconcurrents = int(input("Enter concurrents: "))
        newvip = int(input("Enter 1 for vip, 0 for regular user: "))
        adduser(newtime,newcooldown,newdays,newconcurrents,newvip)
        conn.commit()
    elif s == '3':
        key = input("Enter API key to change")
        ip = input("Enter the IP to whitelist")
        cursor.execute(f"UPDATE users SET whitelist = '{ip}' WHERE apikey = '{key}';")
        conn.commit()
        print("Done...")
    else:
        print("invalid selection")

