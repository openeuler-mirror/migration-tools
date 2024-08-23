#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <math.h>

#include <libssh/libssh.h>
#include <libssh/server.h>
#include <libssh/sftp.h>
#include <sys/stat.h>
#include <sys/utsname.h>
#include <fcntl.h>

int show_remote_processes(ssh_session session, char *cmd);
int authenticate_pubkey(ssh_session session);
//int ssh_command(CHECK_DATA *data, int i, char *sudo, char *yum, char *systemctl, char *mv)
int ssh_command(char *hostadr, char *user, char *password, char *sudo, char *yum, char *systemctl, char *mv, char *mk, char *gp);
