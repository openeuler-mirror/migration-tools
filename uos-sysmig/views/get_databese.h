#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CONF_PATH "/etc/migration-tools/migration-tools.conf"
#define CONF_NAME "migration-tools.conf"

int get_database(char *name,unsigned long **res)
{
        FILE     *input_file;
        unsigned int    file_size = 0;  //读取文件的字节数
        char line[64]; //接收文件每行
        char *buf;
        char *buf0;
	char *pw;
	//memset(*res, 0, sizeof(*res));
        int len = 0;
        int i = 0, j = 0,flag = 0;

        input_file = fopen(CONF_PATH, "rb");
        if (input_file == NULL)
        {
                printf("can not find file!\n");
                return -1;
        }
        while (fgets(line, sizeof(line), input_file))
        {  //用fgets函数逐行读取到line
                char *pLast = strstr(line, name);  //用strrchr查找'='字符最后出现的位置,
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
                                else if(flag==1 && buf[i]=='\"')
                                {
                                        buf0[j]='\0';
					pw = (char*)malloc(sizeof(buf0));
					memset(pw, 0, sizeof(buf0));
					strcpy(pw,buf0);
					//memcpy(pw,buf0,j);
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
