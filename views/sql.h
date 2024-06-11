#define SYS “"/etc/redhat-release"
typedef struct CHECK_DATA
{
    char *ip;
    char *user;
    char *password;
}CHECK_DATA;

MYSQL conn;
MYSQL_RES *res_ptr;
MYSQL_ROW sqlrow;

void connection(const char* db_user, const char* db_password, const char* db_database);
int get_Data(const char* db_user, const char* db_password, const char* db_database, int len, CHECK_DATA *data);
int get_Len(const char* db_user, const char* db_password, const char* db_database, char *sql);

//返回值为负数，执行Sql语句失败
//当执行的为select之类的会有返回数据的sql语句，返回值为获取数据的行数
//当中的为无返回数据的sql语句，如alter、updata等，执行成功返回0
int get_Len(const char* db_user, const char* db_password, const char* db_database, char *sql)
{
	int len = -1, res = 0;
	connection(db_user, db_password, db_database);
	res=mysql_query(&conn, sql);
	if(res)
	{
		mysql_close(&conn);
		return -1;
	}
	if( mysql_affected_rows( &conn ) == 0 ) //执行sql语句改变的行数，0无任何变动，即未达到期望结果，执行失败；大于0执行成功；为-1时，执行的为查询命令
	{
		mysql_close(&conn);
		return -1;
	}
	if( mysql_affected_rows( &conn ) == -1 )
	{
		res_ptr = mysql_store_result(&conn); //获取到的数据
		if(!res_ptr)
		{
			mysql_close(&conn);
			return -1;
		}
		len = (unsigned long)mysql_num_rows(res_ptr); //数据中包括的行数
	}
	else
	{
		mysql_close(&conn);
                return 0;
	}
	mysql_close(&conn);
	return len;
}

int get_Data(const char* db_user, const char* db_password, const char* db_database, int len, CHECK_DATA *data)
{           
        int i = 0, k = 0, res = 0, len0 = 0;
            
           
        connection(db_user, db_password, db_database);
        res = mysql_query(&conn, "select agent_ip, agent_username, AES_DECRYPT(agent_passwd, 'coco')  from agent_info where agent_online_status = 0");
        if(res)//执行sql语句
        {
                len=0;
        }
        else
        { 
                res_ptr = mysql_store_result(&conn);
                len0 = (unsigned long)mysql_num_rows(res_ptr);//获取数据库数据行数
        } 

        if(len != len0)
                len=len0=0;
        else
        {

                for( i=0; i<len ;i++)
                {
                        sqlrow = mysql_fetch_row(res_ptr);

                        k=0;
                        data[i].ip = (char*)malloc(sizeof(char) * strlen(sqlrow[k]));
                        strcpy(data[i].ip,sqlrow[k]);

                        k++;
                        data[i].user = (char*)malloc(sizeof(char) * strlen(sqlrow[k]));
                        strcpy(data[i].user,sqlrow[k]);

                        k++;
                        if ( sqlrow[k] == NULL )
			{
                                data[i].password = (char*)malloc(sizeof(char) * 1);
                                strcpy(data[i].password,"");
                        }
                        else
                        {
                                data[i].password = (char*)malloc(sizeof(char) * strlen(sqlrow[k]));
                                strcpy(data[i].password,sqlrow[k]);
			}
                }
        }
	mysql_close(&conn);

        return 0;
}


void connection(const char* db_user, const char* db_password, const char* db_database) 
{
	system("export LANG=en_US");
	mysql_close(&conn);
    	mysql_init(&conn); // 注意取地址符&

	if (mysql_real_connect(&conn, "localhost", db_user, db_password, db_database, 0, NULL, 0)) 
	{
        	printf("Connection success!\n");
	}
	else
	{
        	fprintf(stderr, "Connection failed!\n");
        	if (mysql_errno(&conn)) 
		{
            		fprintf(stderr, "Connection error %d: %s\n", mysql_errno(&conn), mysql_error(&conn));
        	}
        exit(EXIT_FAILURE);
	}
}
