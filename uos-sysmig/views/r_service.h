#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/utsname.h>
#include <unistd.h>

#define SYS_NAME "/etc/redhat-release"
#define PACK_NAME "uos-sysmig-agent"

int restart_ser(char *yum_shell, char *cp_shell, char *s_ser_shell, char *c_ser_shell, char **sys, char **cpu, char **hostname);

int restart_ser(char *yum_shell, char *cp_shell, char *s_ser_shell, char *c_ser_shell, char **sys, char **cpu, char **hostname)
{
	int yum_res=0;
	int cp_conf=0;
	int s_start=0;
	FILE *f;
        long len;
	struct utsname buf;
	
	if(uname(&buf))
        {
                perror("uname");
                exit(1);
        }
	*cpu=(char*)malloc((sizeof(char))*strlen(buf.machine));
        strcpy(*cpu, buf.machine);

	*hostname=(char*)malloc((sizeof(char))*100);
	gethostname(*hostname, 100);

	f=fopen(SYS_NAME,"rb");
	fseek(f,0,SEEK_END);
	len=ftell(f);
	fseek(f,0,SEEK_SET);
        *sys=(char*)malloc((sizeof(char))*(len));
	fread(*sys,1,len-1,f);
	fclose(f);

	yum_res=system(yum_shell); //yum install -y uos-sysmig-agent
	if(yum_res)
		return 4;//4用于在数据库中标志yum错误
	cp_conf=system(cp_shell);
        if(cp_conf)
                return cp_conf;

	system(s_ser_shell);
        s_start=system(c_ser_shell);
 	if(s_start)
                return 5;//用于在数据库中标志restart服务重启失败
	return 0;
}
