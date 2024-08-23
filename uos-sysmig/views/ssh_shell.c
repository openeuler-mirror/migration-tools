#include "ssh_shell.h"

int ssh_command(char *hostadr, char *user, char *password, char *sudo, char *yum, char *systemctl, char *mv, char *mk, char *gp)
{
	ssh_session my_ssh_session;
	ssh_bind sshbind;

	int rc = 0, ds = 0, pm = 0, pw = 0, dc = 0, run = 0;;
	char *yum_p = NULL;
	char *check_conf = NULL;

        char *ppFld[32];
        char sTmp[64+1];		
	char send_f[256+1];
        char yum_install_agent[256+1];
        char iGetSepFldsnstall_agent_repo[64+1];

	yum_p = (char*)malloc(sizeof(char) * 200);
	check_conf = (char*)malloc(sizeof(char) * 200);

 	sprintf(check_conf, "ls %s", CONF_PATH);

	// Open session and set options
	my_ssh_session = ssh_new();
	sshbind=ssh_bind_new();
	if (my_ssh_session == NULL)
		exit(-1);

	ssh_options_set(my_ssh_session, SSH_OPTIONS_HOST, hostadr);
        ssh_options_set(my_ssh_session, SSH_OPTIONS_USER, user);
	ssh_options_set(my_ssh_session, SSH_OPTIONS_HOSTKEYS, "ssh-rsa");
	// Connect to server
	rc = ssh_connect(my_ssh_session);
	if (rc != SSH_OK)
	{
		fprintf(stderr, "Error connecting to localhost: %s\n", ssh_get_error(my_ssh_session));
		ssh_free(my_ssh_session);
		return 2;
	}
	// Verify the server's identity
	// For the source code of verify_knownhost(), check previous example
	if (verify_knownhost(my_ssh_session) < 0)
	{
		ssh_disconnect(my_ssh_session);
		ssh_free(my_ssh_session);
		return 2;
	}

	// Authenticate ourselves
	ds = 0;
	setenv("SSHPASS","",1);
	rc = ssh_userauth_password(my_ssh_session, NULL, password);
	if (rc != SSH_AUTH_SUCCESS)
	{
		fprintf(stderr, "Error authenticating with password: %s\n", ssh_get_error(my_ssh_session));
		sprintf(yum_p, "sshpass -e ssh -q -t %s@%s ", user, hostadr);
		pw = 2;

		//use pubkey to connect server
		ssh_key pkey;
                ssh_key privkey = ssh_key_new();

		//check the public key
		char *key_path[20];
		sprintf(key_path, "/%s/.ssh/id_rsa.pub", "root");
                rc = ssh_pki_import_pubkey_file(key_path, &pkey);
		if( rc == SSH_OK)
                {
			//verify the public key is available
			//check the privkey key
			sprintf(key_path, "/%s/.ssh/id_rsa", "root");
			rc = ssh_pki_import_privkey_file(key_path, NULL, NULL, NULL, &privkey);
			if(rc == SSH_OK)
			{
				rc = ssh_userauth_publickey(my_ssh_session, NULL, privkey);
				if(rc != SSH_OK)
					ds = 2;
			}
			else
				ds = 2;
		}
		else
			ds = 2;
	}
	else
	{
		sprintf(yum_p, "sshpass -p %s ssh %s@%s ", password, user, hostadr);
	}

	//do shell command
	if(!ds)
	{
		if(strcmp(user,"root"))
			ds=system(sudo);
		if(ds)
			ds = 1;
		else
		{
                        memset(send_f, 0x00, sizeof(send_f));
                        sprintf(send_f, "sshpass -p %s scp %s %s@%s:%s", password, install_agent_repo, user, hostadr);
                        ds = system(send_f);
                        if(ds)
                                //ds = 4;
                                ds = 3;



			
			/*ds = system(yum_p);
			if(ds)
				ds = 4; */
			else
			{
                                //install the Agent Service
                                memset(yum_install_agent, 0x00, sizeof(yum_install_agent));
                                //sprintf(yum_install_agent, "%s \" yum -y install migration-tools-agent -c %s && echo $? \"", yum_p, ppFld[rc-1]);
				sprintf(yum_install_agent, "%s \" yum -y install --disablerepo=* -c %s/%s --enablerepo=uyi* uos-sysmig-agent && echo $? \"", yum_p, agent_repo_dir, ppFld[rc-1]);
                                system(yum_install_agent);

				//scp
			        ds = scp_write(my_ssh_session);
		        	if(ds)
					ds = 3;
			        else
				{
					ds=show_remote_processes(my_ssh_session, mk);
					ds=show_remote_processes(my_ssh_session, mv);
					ds=show_remote_processes(my_ssh_session, check_conf);
					if(ds)
					{
						ds = 3;
						show_remote_processes(my_ssh_session, "rm -f /tmp/migration-tools.conf&&echo $?");
					}
					else
					{
						ds=show_remote_processes(my_ssh_session, systemctl);
                                                if(abs(ds))
                                                {
							//agnet install fail
                                                        ds = 4;
                                                }
                                                else
                                                {
                                                        ds=show_remote_processes(my_ssh_session, "systemctl status migration-tools-agent.service|grep running");
                                                        if(abs(ds))
                                                        {
								//agent restart faile
                                                                ds = 5;
                                                        }
                                                        else
                                                        {
								//agent restart success
                                                                ds = run;
                                                        }
                                                }
					}
				}
			}
		}
	}
        
	//close connect
	//free ssh
	unsetenv("SSHPASS");

	ssh_disconnect(my_ssh_session);
	ssh_free(my_ssh_session);
	free(yum_p);
	yum_p = NULL;
	free(check_conf);
	check_conf = NULL;

	return ds;
}


int verify_knownhost(ssh_session session)
{
#ifdef CENTOS7
    enum ssh_server_known_e state;
#else
    enum ssh_known_hosts_e state;
#endif
    unsigned char *hash = NULL;
    ssh_key srv_pubkey = NULL;
    size_t hlen;
    char buf[10];
    char *hexa;
    char *p;
    int cmp;
    int rc;

#ifdef CENTOS7
	rc = ssh_get_publickey(session, &srv_pubkey);
#else
	rc = ssh_get_server_publickey(session, &srv_pubkey);
#endif
    if (rc < 0) {
        return -1;
    }
    rc = ssh_get_publickey_hash(srv_pubkey,
                                SSH_PUBLICKEY_HASH_SHA1,
                                &hash,
                                &hlen);
    ssh_key_free(srv_pubkey);
    if (rc < 0) {
        return -1;
    }

#ifdef CENTOS7
		state = ssh_is_server_known(session);
		switch (state)
		{
			case SSH_SERVER_KNOWN_OK:
				/* OK */ /*value = 1*/
				 break;

			case SSH_SERVER_KNOWN_CHANGED:
				/*value = 2*/
				fprintf(stderr, "Host key for server changed now\n");
				fprintf(stderr, "For security reasons, connection will be stopped\n");
				ssh_clean_pubkey_hash(&hash);
				//return -1;

			case SSH_SERVER_FOUND_OTHER:
				/*value = 3*/
				fprintf(stderr, "The host key for this server was not found but an other"
				        "type of key exists.\n");
				fprintf(stderr, "An attacker might change the default server key to"
				        "confuse your client into thinking the key does not exist\n");
				ssh_clean_pubkey_hash(&hash);				
				//return -1;

			case SSH_SERVER_FILE_NOT_FOUND:
				/*value = 4*/
				fprintf(stderr, "Could not find known host file.\n");
				fprintf(stderr, "If you accept the host key here, the file will be"
				        "automatically created.\n");
				
				/* FALL THROUGH to SSH_SERVER_NOT_KNOWN behavior */
			case SSH_SERVER_NOT_KNOWN:
				/*value = 0*/
				fprintf(stderr,"The server is unknown. add the host key to known host file\n");
				sprintf(buf,"yes",3);
				cmp = strncasecmp(buf, "yes", 3);
				if (cmp != 0)
				{
	 		               return -1;
				}
				rc = ssh_write_knownhost(session);
				if (rc < 0)
				{
					fprintf(stderr, "Error %s\n", strerror(errno));
					return -1;
				}
				break;
			case SSH_SERVER_ERROR:
				/*value = -1*/
				fprintf(stderr, "Error %s", ssh_get_error(session));
		}
#else
		state = ssh_session_is_known_server(session);
		switch (state)
		{
			case SSH_KNOWN_HOSTS_OK:
				/* OK */ /*value = 1*/
				
				break;
			case SSH_KNOWN_HOSTS_CHANGED:
				/*value = 2*/
				fprintf(stderr, "Host key for server changed now\n");
				fprintf(stderr, "For security reasons, connection will be stopped\n");
				ssh_clean_pubkey_hash(&hash);
				
				return -1;
			case SSH_KNOWN_HOSTS_OTHER:
				/*value = 3*/
				fprintf(stderr, "The host key for this server was not found but an other"
				        "type of key exists.\n");
				fprintf(stderr, "An attacker might change the default server key to"
				        "confuse your client into thinking the key does not exist\n");
				ssh_clean_pubkey_hash(&hash);
				
				return -1;
			case SSH_KNOWN_HOSTS_NOT_FOUND:
				/*value = -1*/
				fprintf(stderr, "Could not find known host file.\n");
				fprintf(stderr, "If you accept the host key here, the file will be"
				        "automatically created.\n");
				
				/* FALL THROUGH to SSH_SERVER_NOT_KNOWN behavior */
				
			case SSH_KNOWN_HOSTS_UNKNOWN:
				/*value = 0*/
				fprintf(stderr,"The server is unknown. add the host key to known host file\n");
				sprintf(buf,"yes",3);
				cmp = strncasecmp(buf, "yes", 3);
				if (cmp != 0) {
				    return -1;
				}
				rc = ssh_session_update_known_hosts(session);
				if (rc < 0) {
				    fprintf(stderr, "Error %s\n", strerror(errno));
				    return -1;
				}
				
				break;
			case SSH_KNOWN_HOSTS_ERROR:
				/*value = -2*/
				fprintf(stderr, "Error %s", ssh_get_error(session));
				ssh_clean_pubkey_hash(&hash);
				return -1;
		}
#endif
	ssh_clean_pubkey_hash(&hash);
	return 0;
}

int show_remote_processes(ssh_session session,char *cmd)
{
	ssh_channel channel;
	int rc;
	char buffer[256];
	int nbytes = 0;

	channel = ssh_channel_new(session);
	if (channel == NULL)
		return SSH_ERROR;

	rc = ssh_channel_open_session(channel);
	if (rc != SSH_OK)
	{
		ssh_channel_free(channel);
		return rc;
	}

	rc = ssh_channel_request_exec(channel, cmd);
	if (rc != SSH_OK)
	{
		ssh_channel_close(channel);
		ssh_channel_free(channel);
		return rc;
	}

	int timeout_ms = 100;
	nbytes = ssh_channel_read_timeout(channel, buffer, sizeof(buffer), 0, timeout_ms);
	if ( nbytes == 0 )
	{
		ssh_channel_close(channel);
		ssh_channel_free(channel);
		return SSH_ERROR;
	}
	while (nbytes > 0)
	{
		if (write(1, buffer, nbytes) != (unsigned int) nbytes)
		{
			ssh_channel_close(channel);
			ssh_channel_free(channel);
			return SSH_ERROR;
		}
		nbytes = ssh_channel_read(channel, buffer, sizeof(buffer), 0);
	}

	ssh_channel_send_eof(channel);
	ssh_channel_close(channel);
	ssh_channel_free(channel);

	return SSH_OK;
}

int scp_write(ssh_session session)
{
	ssh_scp scp;
	int rc;

	scp = ssh_scp_new(session, SSH_SCP_WRITE | SSH_SCP_RECURSIVE, "/tmp");
	if (scp == NULL)
	{
		fprintf(stderr, "Error allocating scp session: %s\n", ssh_get_error(session));
		return SSH_ERROR;
	}
	rc = ssh_scp_init(scp);
	if (rc != SSH_OK)
	{
		fprintf(stderr, "Error initializing scp session: %s\n", ssh_get_error(session));
		ssh_scp_free(scp);
		return rc;
	}

	rc = scp_file(session, scp);
	if(rc != SSH_OK)
	{
		fprintf(stderr, "Error scp files: %s\n", ssh_get_error(session));
		ssh_scp_free(scp);
		return rc;
	}

	ssh_scp_close(scp);
	ssh_scp_free(scp);
	return SSH_OK;
}

int scp_file(ssh_session session, ssh_scp scp)
{
	int rc,tc,yc,uc,ic,oc;
	char *buf;
	long len;
	FILE *f;

	//read conf file to buf
	f=fopen(CONF_PATH,"rb");
	fseek(f,0,SEEK_END);
	len=ftell(f);
	fseek(f,0,SEEK_SET);
	buf=(char*)malloc((sizeof(char))*(len+1));
	fread(buf,1,len+1,f);
	buf[len]='\0';

	//set up directory for scp
	/*rc = ssh_scp_push_directory(scp, "/etc/migration-tools/", S_IRUSR |  S_IWUSR | S_IRGRP | S_IROTH);
        
        
	if (rc != SSH_OK)
	{
		fprintf(stderr, "Can't create remote directory: %s\n", ssh_get_error(session));
		return rc;
	}

	*/

	//touch file for scp 0666
	tc = ssh_scp_push_file(scp, CONF_NAME, len, S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP|S_IROTH|S_IWOTH);
	if (tc != SSH_OK)
	{
		fprintf(stderr, "Can't open remote file: %s\n", ssh_get_error(session));
		free(buf);
		return tc;
	}

	//write buf to scp file
	yc = ssh_scp_write(scp, buf, len);
	free(buf);
        buf = NULL;
	fclose(f);
	if (yc != SSH_OK)
	{
		fprintf(stderr, "Can't write to remote file: %s\n", ssh_get_error(session));
		return yc;
	}

	return SSH_OK;
}

int authenticate_pubkey(ssh_session session)
{
	int rc;

	rc = ssh_userauth_publickey_auto(session, NULL, NULL);

	if (rc == SSH_AUTH_ERROR)
	{
		fprintf(stderr, "Authentication failed: %s\n", ssh_get_error(session));
		return SSH_AUTH_ERROR;
	}

	return rc;
}

