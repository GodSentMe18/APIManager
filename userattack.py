import datetime
from api import METHODS,VIPMETHODS

blacklist = [
    '103.95.221.0',
    '101.71.138.0',
    '117.27.239.0',
    '43.240.204.71',
    '54.38.41.65',
    '142.44.166.226',
    '1.1.1.1',
    '8.8.8.8'
]

USERS = []


def validateint(num,lower,upper):
    try:
        num = int(num)
        if lower <= num <= upper:
            return True
        else:
            raise ValueError
    except ValueError:
        return False
def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

class Attack():
    def __init__(self,duration):
        self.duration = duration
        self.endtime = datetime.datetime.now() + datetime.timedelta(seconds=duration)
class User():
    def __init__(self,key,maxtime,conncurrents,cooldown,isvip,expiry):
        self.lastattack = None
        self.concurrents = int(conncurrents)
        self.maxtime = int(maxtime)
        self.apikey = key
        self.cooldown = int(cooldown)
        self.attacks = []
        self.isvip = isvip
        self.expiry = expiry
        USERS.append(self)
    def sendattack(self,method,host,duration):
        if not validate_ip(host):
            return "Invalid target"
        if host in blacklist:
            return "Target is blacklisted"
        try:
            duration = int(duration)
        except:
            return "Invalid time"
        if method.upper() not in METHODS:
            return "Invalid Method"
        if method.upper() in VIPMETHODS and not self.isvip:
            return "You do not have access to VIP methods"
        if self.lastattack is not None and (self.lastattack + datetime.timedelta(seconds=self.cooldown) > datetime.datetime.now()):
            return f"You have a cooldown of {self.cooldown} seconds"
        for attack in self.attacks:
            if attack.endtime < datetime.datetime.now():
                self.attacks.remove(attack)
        expiry = datetime.datetime.strptime(self.expiry, '%m/%d/%Y')
        if datetime.datetime.now() > expiry:
            return f"Account has expired."
        if len(self.attacks) >= self.concurrents:
            return "You have reached your maximum concurrent attacks"
        if duration > self.maxtime:
            return f"You have a max attack time of {self.maxtime} seconds"
        self.attacks.append(Attack(duration))
        self.lastattack = datetime.datetime.now()
        return "Attack Sent Successfully"