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
	char *f_path;
	const char *home;

        f_host = (char*)malloc(sizeof(char)*100);
        add_host = (char*)malloc(sizeof(char)*100);
	f_path = (char*)malloc(sizeof(char)*100);

	home = getenv("HOME");
	sprintf(f_host, "cat %s/.ssh/known_hosts |grep %s  >> /dev/null  2>&1", home, ip);
        sprintf(add_host, "ssh-keyscan %s >> %s/.ssh/known_hosts ", ip, home);

        sprintf(f_path,"%s/.ssh/known_hosts", home);

	FILE *fp=fopen(f_path,"a+");

	if(fp == NULL)
	{
		fclose(fp);
		add_ip = -1;
	}
	else
	{
		if(system(f_host))
                	add_ip = system(add_host);
	}

        free(f_host);
        free(add_host);
	free(f_path);
	return add_ip;
}


int free_Sec(char *ip, char *user, char *password)
{
	int ssh_key=0;
	int add_sec=0;
	int free_sec=0;
	int ssh_pass=0;
	char *f_sec, *f_sec_bak, *t_sec;
	const char *home;

	home = (char*)malloc(sizeof(char)*100);

	ssh_pass=system("which sshpass");
        if(ssh_pass)
        {
                return -1;
        }

	home = getenv("HOME");
        f_sec_bak = (char*)malloc(sizeof(char)*100);
	sprintf(f_sec_bak, "sshpass -p %s ssh-copy-id -f -i %s/.ssh/id_rsa.pub %s@%s 2>1", password, home, user, ip);

	if(!system(f_sec_bak))
	{
		free(f_sec_bak);
                return 0;
	}
	f_sec = (char*)malloc(sizeof(char)*100);
	t_sec = (char*)malloc(sizeof(char)*100);

        sprintf(f_sec, "sshpass -p %s ssh-copy-id -f -i %s/.ssh/id_rsa.pub %s@%s 2>1", password, home, user, ip);
	sprintf(t_sec, " ssh -tt %s@%s date ", user, ip);

	ssh_key = system("echo -e 'y\n'|ssh-keygen  -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa  2>1");
	if(ssh_key)
		return ssh_key;

	add_sec = system(f_sec);
	free(f_sec);
	if(add_sec)
                        return add_sec;
	free_sec=system(t_sec);
	free(t_sec);
	if(free_sec)
		return free_sec;
	return 0;
}
