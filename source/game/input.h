// search for:
		void		Roulette(LPCHARACTER ch, const char* c_pData);

// add under:
#ifdef __ITEM_SHOP__
		void		ItemShop(LPCHARACTER ch, BYTE header, const char* c_pData);
#endif

// search for:
	void		AffectLoad(LPDESC d, const char * c_pData);

// add under:
#ifdef __ITEM_SHOP__
	void		ItemShopCoinsLoad(LPDESC d, const char * c_pData);
	void		ItemShopItemsLoad(LPDESC d, const char * c_pData);
	void		ItemShopEditorsLoad(LPDESC d, const char * c_pData);
	void		ItemShopItemAdd(LPDESC d, const char * c_pData);
#endif