#define SYS “"/etc/redhat-release"
typedef struct CHECK_DATA
{
    char *ip;
    char *user;
    char *password;
    char *mode;
}CHECK_DATA;

MYSQL conn;
MYSQL_RES *res_ptr;
MYSQL_ROW sqlrow;

void connection(const char* db_user, const char* db_password, const char* db_database);
int get_Data(const char* db_user, const char* db_password, const char* db_database, int len, CHECK_DATA *data);
int get_Len(const char* db_user, const char* db_password, const char* db_database, char *sql);

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
	if( mysql_affected_rows( &conn ) == 0 )
	{
		mysql_close(&conn);
		return -1;
	}
	if( mysql_affected_rows( &conn ) == -1 )
	{
		res_ptr = mysql_store_result(&conn);
		if(!res_ptr)
		{
			mysql_close(&conn);
			return -1;
		}
		len = (unsigned long)mysql_num_rows(res_ptr);
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
        res = mysql_query(&conn, "select agent_ip, agent_username, type, AES_DECRYPT(agent_passwd, 'coco') from agent_info where agent_online_status = 0");
        if(res)
        {
                len=0;
        }
        else
        { 
                res_ptr = mysql_store_result(&conn);
                len0 = (unsigned long)mysql_num_rows(res_ptr);
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
                        data[i].mode = (char*)malloc(sizeof(char) * strlen(sqlrow[k]));
                        strcpy(data[i].mode,sqlrow[k]);

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
	system("export LANG=en_US.UTF-8");
	mysql_close(&conn);
    	mysql_init(&conn);

	if (mysql_real_connect(&conn, "localhost", db_user, db_password, db_database, 0, NULL, 0)) 
        	fprintf(stdin, "Connection success!\n");
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
