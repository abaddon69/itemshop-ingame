// seach for:
		void		HackShieldLog(unsigned long ErrorCode, LPCHARACTER ch);

// add under:
#ifdef __ITEM_SHOP__
		void		ItemShopBuyLog(DWORD dwItemVnum, DWORD dwCount, DWORD dwID, DWORD dwCategory, DWORD dwAccountID, DWORD dwPrice);
#endif