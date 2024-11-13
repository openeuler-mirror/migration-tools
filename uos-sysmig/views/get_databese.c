#include "sql.h"

int get_database(char *file_path, char *name,unsigned long **res)
{
        FILE     *input_file;
        unsigned int    file_size = 0;
        char line[64];
        char *buf;
        char *buf0;
	char *pw;
        int len = 0;
        int i = 0, j = 0,flag = 0;

        input_file = fopen(file_path, "rb");
        if (input_file == NULL)
        {
                printf("can not find file!\n");
                return -1;
        }
        while (fgets(line, sizeof(line), input_file))
        {
                char *pLast = strstr(line, name);
                if (NULL != pLast)
                {
                        len = strlen(pLast)-strlen(name);
                        buf = (char *)malloc(sizeof(char) *len);
                        memcpy(buf,pLast+strlen(name)+1,len);
                        buf0 = (char *)malloc(sizeof(char) *len);

                        while(buf[i]!='\0')
                        {
                                if(flag==0 && buf[i]=='\"')
                                {
                                        flag=1;
                                }
				else if(flag==0)
				{

                                        pw = (char*)malloc(sizeof(buf0));
                                        memset(pw, 0, sizeof(buf0));
					strcpy(pw,buf);
				}
                                else if(flag==1 && buf[i]=='\"')
                                {
                                        buf0[j]='\0';
					pw = (char*)malloc(sizeof(buf0));
					memset(pw, 0, sizeof(buf0));
					strcpy(pw,buf0);
					free(buf0);
		                        buf0 = NULL;
					break;

                                }
                                else if(flag==1 && buf[i]!='\"')
                                {
                                        buf0[j++]=buf[i];
                                }
                                i++;
                                }
                	}
        }
	memcpy(*res,pw,strlen((int *)pw));
        free(pw);
	pw = NULL;
        free(buf);
	buf = NULL;
	return 0;
}
int judge_version()
{
        int cts = 0;
        char *res;
        res = (char *)malloc(sizeof(char) *100);
        get_database(VERSION_PATH,"VERSION_ID", &res);
        if(strstr(res,"7"))
                cts = 7;
	else
	{
		get_database("/etc/os-version","MinorVersion", &res);
		if( strncasecmp(res,"1000",4))
			cts = 7;
		else if( strncasecmp(res,"1020",4))
			cts = 8;
		else if( strncasecmp(res,"1021",4))
			cts = 8;
		else
			printf("not centos 7, 8 or uos 1000, 1020, 1021\n");
	}
        free(res);
        res = NULL;
        return cts;
}
