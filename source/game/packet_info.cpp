// search for:
	Set(HEADER_CG_STATE_CHECKER, sizeof(BYTE), "ServerStateCheck", false);

// add under:
#ifdef __ITEM_SHOP__
	Set(HEADER_CG_ITEMSHOP_OPEN, sizeof(BYTE), "ItemShopOpen", true);
	Set(HEADER_CG_ITEMSHOP_BUY, sizeof(TPacketCGItemShopBuy), "ItemShopBuy", true);
	Set(HEADER_CG_ITEMSHOP_ADD, sizeof(TPacketCGItemShopAddItem), "ItemShopAdd", true);
#endif