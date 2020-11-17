// search for:
typedef enum
{
	SHOP_COIN_TYPE_GOLD, // DEFAULT VALUE
	SHOP_COIN_TYPE_SECONDARY_COIN,
} EShopCoinType;

// add under:
#ifdef __ITEM_SHOP__

enum EItemShopItemFlag
{
	ITEMSHOP_ITEM_FLAG_BOOT,
	ITEMSHOP_ITEM_FLAG_ADD,
	ITEMSHOP_ITEM_FLAG_EDIT
};

#endif