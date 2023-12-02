To deploy, run the command:

```
ansible-playbook -i {ip_here}, -u {user} -k -K deploy_server.yml
```

where `{ip_here}` is the destination server and `{user}` is the remote user used to login. `-k` asks for a SSH password and `-K` asks for a root password (keep blank if the user given has sudo permissions, it will reuse the SSH password in that case).

This script was tested on a base install of Ubuntu Server 22.04.3 LTS
