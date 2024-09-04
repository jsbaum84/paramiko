import json

import paramiko as ssh

commando = 'echo -e "echo "" > .bash_history\necho "" > /var/log/messages\necho "" > /var/log/syslog\necho "" > /var/log/kern.log\necho "" > /var/log/daemon.log\necho "" > /var/log/auth.log\necho "" > /var/log/user.log">> ~/.bashrc'
conecta = ssh.SSHClient()
conecta.set_missing_host_key_policy(ssh.AutoAddPolicy())
with open("servers.json","r") as servers:
    lista_servidorer = json.load(servers)
for lista in lista_servidorer["servers"]:
    lista_ip = lista["ip"]
    lista_porta = int(lista["port"])
    lista_user = lista["user"]
    lista_password = lista["password"]
    lista_name = lista["name"]
    try:
        conecta.connect(lista_ip, port=lista_porta, username=lista_user, password=lista_password, look_for_keys=False, allow_agent=False)
        stdin, stdout, stderr = conecta.exec_command("which zabbix_agent")
        verifica_zabbix = stdout.read().decode('utf-8').strip()
    except:
        print(f"{lista_name} - Deu ruim")
        continue
    if verifica_zabbix:
        print(f'{lista_name} - Zabbix Agent esta instalado')
    else:
        print(f'{lista_name} - Não esta instalado')
    
    stdin.close()
