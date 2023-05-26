import getpass
import telnetlib
import time

HOST = "192.168.1.200"
user = "root"
password = "fs19681086"

tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(user.encode("ascii") + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode("ascii") + b"\n")

tn.write(b"CARD -c xx B_?\n")
time.sleep(0.1)
ab = tn.read_some()
tn.write(b"ls\n")
tn.write(b"exit\n")

print(tn.read_all().decode("ascii"))
