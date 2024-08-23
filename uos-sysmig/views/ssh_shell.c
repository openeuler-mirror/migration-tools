#include "ssh_shell.h"

int ssh_command(char *hostadr, char *user, char *password, char *sudo, char *yum, char *systemctl, char *mv, char *mk, char *gp)
{
	ssh_session my_ssh_session;
	ssh_bind sshbind;

	int rc = 0, ds = 0, pw = 0;
	char *yum_p = NULL;

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

	//close connect
	//free ssh
	unsetenv("SSHPASS");

	ssh_disconnect(my_ssh_session);
	ssh_free(my_ssh_session);
	free(yum_p);
	yum_p = NULL;

	return ds;
}

