#_*_ coding:utf-8 _*_

import Crypto
import paramiko


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.152.128',22,'penguin','123528')
stdin, stdout, stderr = ssh.exec_command('df')
print stdout.read()
ssh.close();
