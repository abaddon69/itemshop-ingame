// search for:
void LogManager::HackShieldLog(unsigned long ErrorCode, LPCHARACTER ch)
{
	[...]
}

// add under:
#ifdef __ITEM_SHOP__
void LogManager::ItemShopBuyLog(DWORD dwItemVnum, DWORD count, DWORD dwID, DWORD dwCategory, DWORD dwAccountID, DWORD dwPrice)
{
	Query( "INSERT INTO itemshop_log%s (account_id, vnum, count, price, id, category, channel, date) VALUES( %d, %d, %d, %d, %d, %d, %d, NOW() )",
			get_table_postfix(),
			dwAccountID, dwItemVnum, count, dwPrice, dwID, dwCategory, g_bChannel);
}
#endif