#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <math.h>

#include "/usr/include/mysql/mysql.h"
#include "/usr/include/mysql/errmsg.h"
#include "/usr/include/mysql/mysqld_error.h"

#define CONF_PATH "/etc/migration-tools/migration-tools.conf"
#define CONF_NAME "migration-tools.conf"
#define PACK_NAME "migration-tools-agent"
#define VERSION_PATH "/etc/os-release"
#define SSH "ssh" 
#define PSW "password"

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

int judge_version();
int get_database(char *file_path, char *name,unsigned long **res);
void connection(const char* db_user, const char* db_password, const char* db_database);
int get_Data(const char* db_user, const char* db_password, const char* db_database, int len, CHECK_DATA *data);
int get_Len(const char* db_user, const char* db_password, const char* db_database, char *sql);
