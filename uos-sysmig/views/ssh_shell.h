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

#define CONF_PATH "/etc/migration-tools/migration-tools.conf"
#define CENTOS7 ((judge_version()!=7)? (0):(1))

int verify_knownhost(ssh_session session);
int show_remote_processes(ssh_session session, char *cmd);
int scp_file(ssh_session session, ssh_scp scp);
int authenticate_pubkey(ssh_session session);
//int ssh_command(CHECK_DATA *data, int i, char *sudo, char *yum, char *systemctl, char *mv)
int ssh_command(char *hostadr, char *user, char *password, char *sudo, char *yum, char *systemctl, char *mv, char *mk, char *gp);
