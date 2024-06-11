int perm_check(char *perm_sql);

int perm_check(char *perm_sql)
{
	int che_res=0;

		che_res=system(perm_sql);
		if(che_res)
		{
			return che_res;
		}
	return 0;
}
