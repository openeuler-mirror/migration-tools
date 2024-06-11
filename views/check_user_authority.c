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

int check_user_authority(char *mode);
int perm_check(char *perm_sql);
int restart_ser(char *yum_shell, char *cp_shell, char *s_ser_shell, char *c_ser_shell, char **sys, char **cpu, char **hostname);
int c_Sec(char *check_sql);
int add_knownhost(char *ip);
int free_Sec(char *ip, char *user, char *password);
int get_database(char *name, char **res);
int get_Data(const char* user, const char* password, const char* database, int len, CHECK_DATA *data);
int get_Len(const char* user, const char* password, const char* database, char *sql);

int check_user_authority(char *mode)
{
	int len = 0,i = 0, num = 0 ;//定义指针存放需要检测的ip
	int do_check = 1;

	char *sys;
	char *cpu;
	char *hostname;

	char *db_user;
	char *u_key="DB_USER";
	char *db_database;
	char *db_key="DB_NAME";
	char *db_password;
	char *pw_key="DB_PASSWORD";

	int do_sql_res=0;//执行sql语句结果
	int password_ssh = 0;//密码是否正确
	int sec = 0; //查询是否免密
	int free_sec_res = 1; //设置免密结果
	int perm_res = 0;	//权限验证结果
	int restart_ser_res; //重启服务结果
	
	char *sql;
	char *check_sql_1;
	char *check_sql_2;
	char *yum_shell;
	char *c_ssh_shell;
	char *perm_shell;
	char *cp_shell;
	char *s_ser_shell;
	char *c_ser_shell;

	//接口输入判断
	if(!(strcmp(mode,SSH)||strcmp(mode,PSW)))
	{
		return 0;
	}

	sql = (char*)malloc(sizeof(char) * 200);
	check_sql_1 = (char*)malloc(sizeof(char) * 100);
	check_sql_2 = (char*)malloc(sizeof(char) * 100);
	c_ssh_shell = (char*)malloc(sizeof(char) * 100);
	perm_shell = (char*)malloc(sizeof(char) * 100);
	yum_shell = (char*)malloc(sizeof(char) * 100);
	cp_shell = (char*)malloc(sizeof(char) * 100);
	s_ser_shell = (char*)malloc(sizeof(char) * 100);
	c_ser_shell = (char*)malloc(sizeof(char) * 100);

	//获取数据库参数
	get_database(u_key,&db_user);
        get_database(pw_key,&db_password);
        get_database(db_key,&db_database);

	//查询在线ip数量
	strcpy(sql, "select agent_ip, agent_username from agent_info where agent_online_status = 0");
	len = get_Len(db_user, db_password, db_database, sql);
        CHECK_DATA data[len];

	if(len > 0)
	{	
		//获取在线ip信息
		get_Data(db_user, db_password, db_database, len, &data);
		//开始验证	
		for( i=0; i<len; i++)
		{
			do_check = 1;
			if(!add_knownhost(data[i].ip))
			{
				sprintf(check_sql_1, "sshpass -p %s_1 ssh %s@%s ls", data[i].password, data[i].user, data[i].ip);
				sec = c_Sec(check_sql_1);
			}
			if(sec)
			{
				sprintf(check_sql_2, "sshpass -p %s ssh %s@%s ls", data[i].password, data[i].user, data[i].ip);
				if(c_Sec(check_sql_2))
				{
					sprintf(sql, "update agent_info set agent_online_status =2 where agent_ip = \"%s\"", data[i].ip);//未免密，且密码错误
					do_check=0;
				}
				else
				{
					if(!strcmp(mode,SSH))
					{
						free_sec_res=free_Sec(data[i].ip, data[i].user, data[i].password);//调用免密函数
						if(free_sec_res)
						{
							sprintf(sql, "update agent_info set agent_online_status =3 where agent_ip = \"%s\"", data[i].ip);//免密失败
						      	do_check=0;
						}
					}
					else
					{
						sprintf(c_ssh_shell, "sshpass -p  %s ssh %s@%s ls", data[i].password, data[i].user, data[i].ip);
                                               	sprintf(perm_shell, "sshpass -p %s ssh %s@%s sudo -v", data[i].password, data[i].user, data[i].ip);
                                          	sprintf(yum_shell, "sshpass -p %s ssh %s@%s yum install -y %s", data[i].password, data[i].user, data[i].ip, PACK_NAME);
						sprintf(cp_shell, "sshpass -p %s scp %s %s@%s:%s", data[i].password, CONF_NAME, data[i].user, data[i].ip, CONF_NAME);
						sprintf(s_ser_shell, "sshpass -p %s ssh %s@%s systemctl restart %s.service", data[i].password, data[i].user, data[i].ip, PACK_NAME);
						sprintf(c_ser_shell,"sshpass -p %s ssh %s@%s systemctl status %s.service |grep running", data[i].password, data[i].user, data[i].ip, PACK_NAME);
					}
				}
			}
			if(!sec || !free_sec_res)
			{
					sprintf(perm_shell, "ssh %s@%s sudo -v", data[i].user, data[i].ip);
					sprintf(yum_shell, "ssh %s@%s yum install -y %s", data[i].user, data[i].ip, PACK_NAME);
					sprintf(cp_shell, "scp %s %s@%s:%s", CONF_NAME, data[i].user, data[i].ip, CONF_NAME);
					sprintf(s_ser_shell, "ssh %s@%s systemctl restart %s.service", data[i].user, data[i].ip, PACK_NAME);
					sprintf(c_ser_shell,"ssh %s@%s systemctl status %s.service |grep running", data[i].user, data[i].ip, PACK_NAME);				
			}
			if(do_check)
			{
				if( data[i].user  != "root" )
					perm_res=perm_check(perm_shell);
				if(perm_res)
					sprintf(sql, "update agent_info set agent_online_status =1 where agent_ip = \"%s\"", data[i].ip);//权限检测失败
				restart_ser_res=restart_ser(yum_shell, cp_shell, s_ser_shell, c_ser_shell, &sys, &cpu, &hostname); //重启uos-sysmig-agent.service服务

				if(!(perm_res ||restart_ser_res))
				{
					sprintf(sql, "update agent_info set agent_os =\"%s\", agent_arch = \"%s\", hostname = \"%s\" where agent_ip = \"%s\"", sys, cpu, hostname, data[i].ip);
					//sql语句,更新数据库system、cpu、hostname
					num++;
					free(sys);
					sys = NULL;
					free(cpu);
					cpu = NULL;
					free(hostname);
					hostname = NULL;
				}
				if(!perm_res && restart_ser_res)
				{
					sprintf(sql, "update agent_info set agent_online_status =%d where agent_ip = \"%s\"",restart_ser_res, data[i].ip);//在数据库中标志重启服务失败具体错误原因
				}
			}
			get_Len(db_user, db_password, db_database, sql);
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
	free(perm_shell);
	perm_shell = NULL;
	free(sql);
	free(check_sql_1);
	free(check_sql_2);
	check_sql_2 = NULL;
	return num;

}
