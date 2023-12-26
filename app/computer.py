class Computer:
    name: str
    mac: str
    ip: str
    status:str
    
    def __init__(self,name:str,mac:str,ip:str,status:str = "offline"):
        self.name = name
        self.mac = mac
        self.ip = ip
        self.status = status