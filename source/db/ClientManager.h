// search for:
	void		RESULT_AFFECT_LOAD(CPeer * pkPeer, MYSQL_RES * pRes, DWORD dwHandle);

// add under:
#ifdef __ITEM_SHOP__
	void		RESULT_ITEMSHOP_COINS_LOAD(CPeer * pkPeer, MYSQL_RES * pRes, DWORD dwHandle);
#endif

// search for:
#ifdef __AUCTION__
	void EnrollInAuction (CPeer * peer, DWORD owner_id, AuctionEnrollProductInfo* data);
	[...]
#endif

// add under:
#ifdef __ITEM_SHOP__
	void QUERY_ITEMSHOP_ITEMS_LOAD(CPeer * pkPeer, DWORD dwHandle);
	void RESULT_ITEMSHOP_ITEMS_LOAD(CPeer * pkPeer, SQLMsg * msg);
	void QUERY_ITEMSHOP_UPDATE_COINS(TItemShopSetCoins * p);
	void QUERY_ITEMSHOP_DELETE_ITEM(TItemShopDeleteItem * p);
	void QUERY_ITEMSHOP_ITEM_ADD(CPeer * pkPeer, TItemShopEdit * p);
	void QUERY_ITEMSHOP_EDITORS_LOAD(CPeer * pkPeer, DWORD dwHandle);
	void RESULT_ITEMSHOP_EDITORS_LOAD(CPeer * pkPeer, SQLMsg * msg);
#endif