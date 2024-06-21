#include <stdio.h>
#include <stdlib.h>

int free_Sec(char *ip, char *user, char *password);
int add_knownhost(char *ip);
int c_Sec(char *check_sql);

int c_Sec(char *check_sql)
{
        if(system(check_sql))
                return 1;            
        return 0;
}


int add_knownhost(char *ip)
{
	int add_ip = 0;
	char *f_host, *add_host;

        f_host = (char*)malloc(sizeof(char)*100);
        add_host = (char*)malloc(sizeof(char)*100);
	sprintf(f_host, "cat ~/.ssh/known_hosts |grep %s", ip);
        sprintf(add_host, "ssh-keyscan %s >> ~/.ssh/known_hosts", ip);

	if(system(f_host))//与agent_ip没有连接过
                add_ip = system(add_host);//添加agentip

        free(f_host);
        free(add_host);
	return add_ip;
}


int free_Sec(char *ip, char *user, char *password)
{
	int ssh_key=0;
	int add_sec=0;
	int free_sec=0;
	int ssh_pass=0;
	char *f_sec, *f_sec_bak, *t_sec;

	ssh_pass=system("which sshpass");
        if(ssh_pass)
        {
                return -1;
        }

        f_sec_bak = (char*)malloc(sizeof(char)*100);
	sprintf(f_sec_bak, "sshpass -p %s ssh-copy-id -f -i $HOME/.ssh/id_rsa.pub %s@%s", password, user, ip);

	if(!system(f_sec_bak))
	{
		free(f_sec_bak);
                return 0;
	}
	f_sec = (char*)malloc(sizeof(char)*100);
	t_sec = (char*)malloc(sizeof(char)*100);

        sprintf(f_sec, "sshpass -p %s ssh-copy-id -f -i $HOME/.ssh/id_rsa.pub %s@%s", password, user, ip);
	sprintf(t_sec, " ssh -tt %s@%s ls ", user, ip);

	ssh_key = system("echo -e 'y\n'|ssh-keygen  -t rsa -b 2048 -N '' -f $HOME/.ssh/id_rsa");//强制重新生成密钥
	if(ssh_key)
		return ssh_key;

	add_sec = system(f_sec);//设置免密
	free(f_sec);
	if(add_sec)
                        return add_sec;
	free_sec=system(t_sec);//验证免密
	free(t_sec);
	if(free_sec)
		return free_sec;
	return 0;
}
