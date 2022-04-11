#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define PACK_NAME "uos-sysmig-agent"

int restart_ser(char *yum_shell, char *cp_shell, char *mv_shell, char *s_ser_shell, char *c_ser_shell);

int restart_ser(char *yum_shell, char *cp_shell, char *mv_shell, char *s_ser_shell, char *c_ser_shell)
{
	int yum_res=0;
	int cp_conf=0;
	int mv_conf=0;
	int s_start=0;
	
	yum_res=system(yum_shell); //yum install -y uos-sysmig-agent
	if(yum_res)
		return 4;//4用于在数据库中标志yum错误
	cp_conf=system(cp_shell);
        if(cp_conf)
                return 5;

	mv_conf=system(mv_shell);
        if(mv_conf)
                return 5;

	system(s_ser_shell);
        s_start=system(c_ser_shell);
 	if(s_start)
                return 5;//用于在数据库中标志restart服务重启失败
	return 0;
}
