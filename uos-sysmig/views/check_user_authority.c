#include    <stdio.h>
#include    <string.h>
#include    <stdlib.h>
#include    <math.h>
#include "/usr/include/mysql/mysql.h"
#include "/usr/include/mysql/errmsg.h"
#include "/usr/include/mysql/mysqld_error.h"

#include "sql.h"
#include "r_service.h"
#include "p_check.h"
#include "f_sec.h"
#include "get_databese.h"

////const char __invoke_dynamic_linker__[] __attribute__ ((section (".interp"))) = "/lib64/ld-linux-x86-64.so.2";

#define SSH "ssh" 
#define PSW "password"

int check_user_authority(void);
int perm_check(char *perm_sql);
int restart_ser(char *yum_shell, char *cp_shell, char *mv_shell, char *s_ser_shell, char *c_ser_shell);
int c_Sec(char *check_sql);
int add_knownhost(char *ip);
int free_Sec(char *ip, char *user, char *password);
int get_database(char *name, unsigned long **res);
int get_Data(const char* db_user, const char* db_password, const char* db_database, int len, CHECK_DATA *data);
int get_Len(const char* user, const char* password, const char* database, char *sql);

int check_user_authority(void)
{
	int len = 0,i = 0, num = 0 ;
	int do_check = 0;

	char *db_user;
	unsigned long *db_pwd;
	char *u_key="DB_USER";
	char *db_database;
	unsigned long *db_pwd1;
	char *db_key="DB_NAME";
	char *db_password;
	unsigned long *db_pwd2;
	char *pw_key="DB_PASSWORD";

	int r_psw = 0;
	int do_sql_res=0;
	int password_ssh = 0;
	int sec = 0;
	int free_sec_res = 0;
	int perm_res = 0;
	int restart_ser_res;
	
	char *sql;
	char *check_sql_1;
	char *check_sql_2;
	char *yum_shell;
	char *c_ssh_shell;
	char *perm_shell;
	char *perm_shell_1;
	char *cp_shell;
	char *mv_shell;
	char *s_ser_shell;
	char *c_ser_shell;

	sql = (char*)malloc(sizeof(char) * 200);
	check_sql_1 = (char*)malloc(sizeof(char) * 100);
	check_sql_2 = (char*)malloc(sizeof(char) * 100);
	c_ssh_shell = (char*)malloc(sizeof(char) * 100);
	perm_shell = (char*)malloc(sizeof(char) * 100);
	perm_shell_1 = (char*)malloc(sizeof(char) * 200);
	yum_shell = (char*)malloc(sizeof(char) * 200);
	cp_shell = (char*)malloc(sizeof(char) * 200);
	mv_shell = (char*)malloc(sizeof(char) * 200);
	s_ser_shell = (char*)malloc(sizeof(char) * 200);
	c_ser_shell = (char*)malloc(sizeof(char) * 200);
	db_pwd =  (unsigned long*)malloc(sizeof(unsigned long) * 20);
	memset(db_pwd, 0, 20);
	db_pwd1 =  (unsigned long*)malloc(sizeof(unsigned long) * 20);
        memset(db_pwd1, 0, 20);
	db_pwd2 =  (unsigned long*)malloc(sizeof(unsigned long) * 20);
        memset(db_pwd2, 0, 20);

	fflush(stdout);
	get_database(u_key,&db_pwd);
	db_user = (char*)malloc(sizeof(char) * (strlen((char *)db_pwd)+1));
	//memcpy(db_user, (char *)db_pwd, strlen((char *)db_pwd));
	strcpy(db_user, (char *)db_pwd);
	free(db_pwd);
	db_pwd = NULL;

	//fflush(stdout);
	get_database(db_key,&db_pwd1);
        db_database = (char*)malloc(sizeof(char) * (strlen((char *)db_pwd1)+1));
        //memcpy(db_user, (char *)db_pwd, strlen((char *)db_pwd));
        strcpy(db_database, (char *)db_pwd1);
        free(db_pwd1);
	db_pwd1 = NULL;

	fflush(stdout);
        get_database(pw_key,&db_pwd2);
        db_password = (char*)malloc(sizeof(char) * (strlen((char *)db_pwd2)+1));
        //memcpy(db_user, (char *)db_pwd, strlen((char *)db_pwd));
        strcpy(db_password, (char *)db_pwd2);
	free(db_pwd2);
	db_pwd2 = NULL;

	strcpy(sql, "select agent_ip, agent_username from agent_info where agent_online_status = 0");
	len = get_Len(db_user, db_password, db_database, sql);
       	CHECK_DATA data[len];
	if(len > 0)
	{	
		setenv("LANG","en_US.UTF-8",1);
		get_Data(db_user, db_password, db_database, len, &data);
		for( i=0; i<len; i++)
		{
			do_check = 0;
	        	if(strcmp(data[i].mode,SSH)||strcmp(data[i].mode,PSW))
			{
				if(!add_knownhost(data[i].ip))
				{
					sprintf(check_sql_1, "sshpass -e ssh -q -t %s@%s date >> /dev/null  2>&1 ", data[i].user, data[i].ip);
					setenv("SSHPASS","",1); 
					sec = c_Sec(check_sql_1);
					unsetenv("SSHPASS");

				}
				else
					do_check = 1;
				if(sec)
				{
					sprintf(check_sql_2, "sshpass -p %s ssh  %s@%s date >> /dev/null  2>&1 ", data[i].password, data[i].user, data[i].ip);
					r_psw = c_Sec(check_sql_2);
					if(r_psw)
						do_check = 1;
					else
					{
						if(!strcmp(data[i].mode,SSH))
						{
							free_sec_res=free_Sec(data[i].ip, data[i].user, data[i].password);
							if(free_sec_res)
								do_check = 1;
							else
								sec = 0;
						}
						else
						{
							if(!strcmp(data[i].user,"root"))
							{
								sprintf(c_ssh_shell, "sshpass -p  %s ssh %s@%s date", data[i].password, data[i].user, data[i].ip);
                                                        	sprintf(yum_shell, "sshpass -p %s ssh %s@%s yum install -y %s >> /dev/null  2>&1", data[i].password, data[i].user, data[i].ip, PACK_NAME);
                                                        	sprintf(cp_shell, "sshpass -p %s scp %s %s@%s:%s", data[i].password, CONF_PATH, data[i].user, data[i].ip, "/tmp");
                                                        	sprintf(mv_shell, "sshpass -p %s ssh %s@%s mv %s/%s %s >> /dev/null  2>&1 ", data[i].password, data[i].user, data[i].ip, "/tmp", CONF_NAME, CONF_PATH);
                                                        	sprintf(s_ser_shell, "sshpass -p %s ssh %s@%s systemctl restart %s.service >> /dev/null  2>&1", data[i].password, data[i].user, data[i].ip, PACK_NAME);
                                                        	sprintf(c_ser_shell,"sshpass -p %s ssh %s@%s \" systemctl status %s.service |grep running >> /dev/null  2>&1 \"", data[i].password, data[i].user, data[i].ip, PACK_NAME);
							}
							else
							{
								sprintf(c_ssh_shell, "sshpass -p  %s ssh %s@%s date", data[i].password, data[i].user, data[i].ip);
								sprintf(perm_shell, "sshpass -p %s ssh %s@%s \" sudo -v >> /dev/null  2>&1 \"", data[i].password, data[i].user, data[i].ip);
								sprintf(perm_shell_1,"sshpass -p %s ssh %s@%s \" echo '%s\n'|sudo -S -l -U %s >> /dev/null  2>&1 \"", data[i].password, data[i].user, data[i].ip, data[i].password, data[i].user);
                                                        	sprintf(yum_shell, "sshpass -p %s ssh %s@%s \" echo '%s\n'|sudo -S yum install -y %s >> /dev/null  2>&1\"", data[i].password, data[i].user, data[i].ip, data[i].password, PACK_NAME);
								sprintf(cp_shell, "sshpass -p %s scp %s %s@%s:%s", data[i].password, CONF_PATH, data[i].user, data[i].ip, "/tmp");
								sprintf(mv_shell, "sshpass -p %s ssh %s@%s \" echo '%s\n'|sudo -S mv %s/%s %s >> /dev/null  2>&1\" ", data[i].password, data[i].user, data[i].ip, data[i].password, "/tmp", CONF_NAME, CONF_PATH);
								sprintf(s_ser_shell, "sshpass -p %s ssh %s@%s \" echo '%s\n'|sudo -S systemctl restart %s.service >> /dev/null  2>&1\"", data[i].password, data[i].user, data[i].ip, data[i].password, PACK_NAME);
                                                       		sprintf(c_ser_shell,"sshpass -p %s ssh %s@%s \" systemctl status %s.service |grep running >> /dev/null  2>&1 \"", data[i].password, data[i].user, data[i].ip, PACK_NAME);
							}
						}
					}			
				}
				if(!sec)
				{
					if(!strcmp(data[i].user,"root"))
					{
                                        	sprintf(yum_shell, "ssh %s@%s yum install -y %s >> /dev/null  2>&1", data[i].user, data[i].ip, PACK_NAME);
						sprintf(cp_shell, "scp %s %s@%s:%s", CONF_PATH, data[i].user, data[i].ip, "/tmp");
                                        	sprintf(mv_shell, "ssh %s@%s mv %s/%s %s >> /dev/null  2>&1 ", data[i].user, data[i].ip, "/tmp", CONF_NAME, CONF_PATH);
						sprintf(s_ser_shell, "ssh %s@%s systemctl restart %s.service >> /dev/null  2>&1", data[i].user, data[i].ip, PACK_NAME);
                                        	sprintf(c_ser_shell,"ssh %s@%s \" systemctl status %s.service |grep running >> /dev/null  2>&1 \"", data[i].user, data[i].ip, PACK_NAME);
					}
					else
					{
						sprintf(perm_shell, "ssh %s@%s \" sudo -v >> /dev/null  2>&1\"", data[i].user, data[i].ip);
                                                sprintf(perm_shell_1,"ssh %s@%s \" echo '%s\n'|sudo -S -l -U %s >> /dev/null  2>&1\"", data[i].user, data[i].ip, data[i].password, data[i].user);
                                                sprintf(yum_shell, "ssh %s@%s \" echo '%s\n'|sudo -S yum install -y %s >> /dev/null  2>&1\"", data[i].user, data[i].ip,  data[i].password, PACK_NAME);
                                                sprintf(cp_shell, "scp %s %s@%s:%s", CONF_PATH, data[i].user, data[i].ip, "/tmp");
                                                sprintf(mv_shell, "ssh %s@%s \" echo '%s\n'|sudo -S mv %s/%s %s >> /dev/null  2>&1\" ", data[i].user, data[i].ip, data[i].password, "/tmp", CONF_NAME, CONF_PATH);
                                                sprintf(s_ser_shell, "ssh %s@%s \" echo '%s\n'|sudo -S systemctl restart %s.service >> /dev/null  2>&1\"", data[i].user, data[i].ip, data[i].password, PACK_NAME);
                                                sprintf(c_ser_shell,"ssh %s@%s \" systemctl status %s.service |grep running >> /dev/null  2>&1 \"", data[i].user, data[i].ip, PACK_NAME);
					}
				}

				if(do_check)
					sprintf(sql, "update agent_info set agent_online_status =2, agent_history_faild_reason = \"agent password error\" where agent_ip = \"%s\"", data[i].ip);
				else
				{
					if(strcmp(data[i].user,"root"))
					{
						perm_res=perm_check(perm_shell);
						if(perm_res)
							perm_res=perm_check(perm_shell_1);
					}
					if(perm_res)
						sprintf(sql, "update agent_info set agent_online_status =1, agent_history_faild_reason = \"agent check permssion failed\" where agent_ip = \"%s\" and agent_username = \"%s\"", data[i].ip, data[i].user);
					else
					{
						restart_ser_res=restart_ser(yum_shell, cp_shell, mv_shell, s_ser_shell, c_ser_shell);
						if (restart_ser_res ==4)
							sprintf(sql, "update agent_info set agent_online_status =%d, agent_history_faild_reason = \"agent install package failed\" where agent_ip = \"%s\" and agent_username = \"%s\"",restart_ser_res, data[i].ip,  data[i].user);
						else if (restart_ser_res ==5)
							sprintf(sql, "update agent_info set agent_online_status =%d, agent_history_faild_reason = \"agent restart service failed\" where agent_ip = \"%s\" and agent_username = \"%s\"",restart_ser_res, data[i].ip, data[i].user);
						else {
							sprintf(sql, "update agent_info set agent_online_status =%d, agent_history_faild_reason = NULL where agent_ip = \"%s\" and agent_username = \"%s\"",restart_ser_res, data[i].ip, data[i].user);
							num++;
						}
					}
				}
				get_Len(db_user, db_password, db_database, sql);
			}
		}
	}
	for(i=0; i<len; i++)
	{
		free(data[i].ip);
		data[i].ip = NULL;
		free(data[i].user);
		data[i].user = NULL;
		free(data[i].password);
		data[i].password = NULL;
		free(data[i].mode);
                data[i].mode = NULL;
	}
	free(db_user);
	db_user = NULL;
	free(db_password);
	db_password = NULL;
	free(db_database);
	db_database = NULL;
	free(c_ser_shell);
	c_ser_shell = NULL;
	free(s_ser_shell);
	s_ser_shell = NULL;
	free(yum_shell);
	yum_shell = NULL;
	free(cp_shell);
	cp_shell = NULL;
        free(mv_shell);
        mv_shell = NULL;
	free(perm_shell);
	perm_shell = NULL;
	free(perm_shell_1);
        perm_shell_1 = NULL;
	free(sql);
	sql = NULL;
	free(check_sql_1);
	check_sql_1 = NULL;
	free(check_sql_2);
	check_sql_2 = NULL;
	fflush(stdout);
	return num;

}
