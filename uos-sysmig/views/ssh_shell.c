#include "ssh_shell.h"

int ssh_command(char *hostadr, char *user, char *password, char *sudo, char *yum, char *systemctl, char *mv, char *mk, char *gp)
{
	ssh_session my_ssh_session;
	ssh_bind sshbind;

	int rc = 0, ds = 0, pw = 0 ;
	char *yum_p = NULL;

        char *ppFld[32];
        char sTmp[64+1];		
	char send_f[256+1];
        char yum_install_agent[256+1];

	yum_p = (char*)malloc(sizeof(char) * 200);

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
                                ds = 3;
			else
			{
                                //install the Agent Service
                                memset(yum_install_agent, 0x00, sizeof(yum_install_agent));
                                //sprintf(yum_install_agent, "%s \" yum -y install migration-tools-agent -c %s && echo $? \"", yum_p, ppFld[rc-1]);
				sprintf(yum_install_agent, "%s \" yum -y install --disablerepo=* -c %s/%s --enablerepo=uyi* migration-tools-agent && echo $? \"", yum_p, agent_repo_dir, ppFld[rc-1]);
                                system(yum_install_agent);

		        	if(ds)
					ds = 3;
			        else
				{
					ds=show_remote_processes(my_ssh_session, mk);
					ds=show_remote_processes(my_ssh_session, mv);
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

	return ds;
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


