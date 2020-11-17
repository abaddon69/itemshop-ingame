// search for:
void SetPlayerDBName(const char* c_pszPlayerDBName);

// add under:
#ifdef __ITEM_SHOP__
void SetAccountDBName(const char* c_pszAccountDBName);
#endif

// search for:
std::string g_stPlayerDBName = "";

// add under:
#ifdef __ITEM_SHOP__
std::string g_stAccountDBName = "";
#endif

// search for:
		fprintf(stderr, "Success ACCOUNT\n");

// add under:
#ifdef __ITEM_SHOP__
		SetAccountDBName(szDB);
#endif

// search for:
const char * GetPlayerDBName()
{
	[...]
}

// add under:
#ifdef __ITEM_SHOP__
void SetAccountDBName(const char* c_pszAccountDBName)
{
	if (! c_pszAccountDBName || ! *c_pszAccountDBName)
		g_stAccountDBName = "";
	else
	{
		g_stAccountDBName = c_pszAccountDBName;
		g_stAccountDBName += ".";
	}
}

const char * GetAccountDBName()
{
	return g_stAccountDBName.c_str();
}
#endif