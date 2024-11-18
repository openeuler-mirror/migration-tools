#include "check_user_authority.h"

int check_user_authority(void)
{
	int len = 0,i = 0, num = 0 ;

	char *db_user;
	unsigned long *db_pwd;
	char *u_key="DB_USER";
	char *db_database;
	unsigned long *db_pwd1;
	char *db_key="DB_NAME";
	char *db_password;
	unsigned long *db_pwd2;
	char *pw_key="DB_PASSWORD";

	int up_sql = 0;
	int r_psw = 0;
	int do_sql_res=0;
	int password_ssh = 0;
	int sec = 0;
	int free_sec_res = 0;
	int perm_res = 0;
	int restart_ser_res;
	
	char *sql;

	sql = (char*)malloc(sizeof(char) * 200);
	db_pwd =  (unsigned long*)malloc(sizeof(unsigned long) * 20);
	memset(db_pwd, 0, 20);
	db_pwd1 =  (unsigned long*)malloc(sizeof(unsigned long) * 20);
        memset(db_pwd1, 0, 20);
	db_pwd2 =  (unsigned long*)malloc(sizeof(unsigned long) * 20);
        memset(db_pwd2, 0, 20);

	fflush(stdout);
	get_database(CONF_PATH, u_key, &db_pwd);
	db_user = (char*)malloc(sizeof(char) * (strlen((char *)db_pwd)+1));
	//memcpy(db_user, (char *)db_pwd, strlen((char *)db_pwd));
	strcpy(db_user, (char *)db_pwd);
	free(db_pwd);
	db_pwd = NULL;

	//fflush(stdout);
	get_database(CONF_PATH, db_key, &db_pwd1);
        db_database = (char*)malloc(sizeof(char) * (strlen((char *)db_pwd1)+1));
        //memcpy(db_user, (char *)db_pwd, strlen((char *)db_pwd));
        strcpy(db_database, (char *)db_pwd1);
        free(db_pwd1);
	db_pwd1 = NULL;

	fflush(stdout);
        get_database(CONF_PATH, pw_key, &db_pwd2);
        db_password = (char*)malloc(sizeof(char) * (strlen((char *)db_pwd2)+1));
        //memcpy(db_user, (char *)db_pwd, strlen((char *)db_pwd));
        strcpy(db_password, (char *)db_pwd2);
	free(db_pwd2);
	db_pwd2 = NULL;

        char *sudo = NULL;
        char *yum = NULL;
        char *systemctl = NULL;
        char *mv = NULL;
	char *mk = NULL;
	char *gp = NULL;

        sudo = (char*)malloc(sizeof(char) * 100);
	mk = (char*)malloc(sizeof(char) * 100);
        mv = (char*)malloc(sizeof(char) * 100);
        yum = (char*)malloc(sizeof(char) * 200);
        systemctl = (char*)malloc(sizeof(char) * 200);
        gp = (char*)malloc(sizeof(char) * 200);

	strcpy(sql, "select agent_ip, agent_username from agent_info where agent_online_status = 0");
	len = get_Len(db_user, db_password, db_database, sql);
       	CHECK_DATA data[len];
	if(len > 0)
	{	
		setenv("LANG","en_US.UTF-8",1);
		get_Data(db_user, db_password, db_database, len, &data);
		for (i=0;i<len;i++)
		{
                	if(strcmp(data[i].mode,"ssh")||strcmp(data[i].mode,"password"))
                	{
                        	if(!strcmp(data[i].user,"root"))
                        	{
					sprintf(gp, "grep VERSION_ID /etc/os-release | awk -F '\\\"' '{print $2}'");
					sprintf(mk, "mkdir -p /etc/migration-tools && echo $?");
					sprintf(mv, "mv -f %s/%s %s && echo $?", "/tmp", CONF_NAME, CONF_PATH);
                                	sprintf(yum, "yum install %s -y ", PACK_NAME);
                                	sprintf(systemctl, "systemctl %s %s.service && echo success", "restart", PACK_NAME);
                        	}
                        	else
                        	{
					sprintf(gp, "echo '%s\n'|sudo -S grep VERSION_ID /etc/os-release | awk -F '\\\"' '{print $2}'", data[i].password);
					sprintf(mk, "echo '%s\n'|sudo -S mkdir -p /etc/%s && echo $?", data[i].password, "migration-tools");
					sprintf(sudo, "sshpass -p %s ssh %s@%s \"echo '%s'|sudo -S -v\"", data[i].password, data[i].user, data[i].ip, data[i].password);
					sprintf(mv, "echo '%s\n'|sudo -S mv -f %s/%s %s && echo $?", data[i].password, "/tmp", CONF_NAME, CONF_PATH);
                                	sprintf(yum, "echo '%s\n'|sudo -S yum install %s -y ", data[i].password, PACK_NAME);
                                	sprintf(systemctl, "echo '%s\n'|sudo -S systemctl %s %s.service && echo $?", data[i].password, "restart", PACK_NAME);
                        	}
                        	up_sql = ssh_command(data[i].ip, data[i].user, data[i].password, sudo, yum, systemctl, mv, mk, gp);
				switch(up_sql)
				{
					case 0:
						sprintf(sql, "update agent_info set agent_online_status =%d, agent_history_faild_reason =NULL where agent_ip = \"%s\" and agent_username = \"%s\"", up_sql, data[i].ip, data[i].user);
                                                num++;
						break;
					case 1:
						sprintf(sql, "update agent_info set agent_online_status =%d, agent_history_faild_reason = \"insufficent agent user permissions\" where agent_ip = \"%s\" and agent_username = \"%s\"", F_IMPORT, data[i].ip, data[i].user);
						break;
					case 2:
						sprintf(sql, "update agent_info set agent_online_status =%d, agent_history_faild_reason = \"agent can not connect server\" where agent_ip = \"%s\" and agent_username = \"%s\"", F_IMPORT, data[i].ip, data[i].user);
						break;
                                        case 3:
                                                sprintf(sql, "update agent_info set agent_online_status =%d, agent_history_faild_reason = \"can not find conf file\" where agent_ip = \"%s\" and agent_username = \"%s\"", F_IMPORT, data[i].ip, data[i].user);
                                                break;
					case 4:
						sprintf(sql, "update agent_info set agent_online_status =%d, agent_history_faild_reason = \"agent can not yum packages\" where agent_ip = \"%s\" and agent_username = \"%s\"", F_IMPORT, data[i].ip, data[i].user);
						break;
					case 5:
						sprintf(sql, "update agent_info set agent_online_status =%d, agent_history_faild_reason = \"agent restart service failed\" where agent_ip = \"%s\" and agent_username = \"%s\"", F_IMPORT, data[i].ip, data[i].user);
						break;
					default:
						sprintf(sql, "update agent_info set agent_online_status =%d, agent_history_faild_reason =NULL where agent_ip = \"%s\" and agent_username = \"%s\"", up_sql, data[i].ip, data[i].user);
				}
				get_Len(db_user, db_password, db_database, sql);
                	}

        	}
	}







	for(i=0;i<len;i++)
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
	free(sql);
	sql = NULL;


	free(sudo);
        sudo = NULL;
	free(mk);
        mk = NULL;
        free(mv);
        mv = NULL;
        free(yum);
        gp = NULL;
        free(gp);
        yum = NULL;
        free(systemctl);
        systemctl = NULL;

	fflush(stdout);
	return num;

}
