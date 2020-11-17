// search for:
	HEADER_CG_QUEST_CONFIRM			= 31,

// add under:
#ifdef __ITEM_SHOP__
	HEADER_CG_ITEMSHOP_OPEN						= 32,
	HEADER_CG_ITEMSHOP_BUY						= 33,
	HEADER_CG_ITEMSHOP_ADD						= 39,
#endif

// search for:
	HEADER_GC_MAIN_CHARACTER4_BGM_VOL	= 138,
	// END_OF_SUPPORT_BGM

// add under:
#ifdef __ITEM_SHOP__
	HEADER_GC_ITEMSHOP				= 139,
#endif

// search for:
typedef struct SPacketGCStateCheck
{
	[...]
} TPacketGCStateCheck;

// add under:
#ifdef __ITEM_SHOP__
enum
{
	ITEMSHOP_SUBHEADER_GC_ITEM,
	ITEMSHOP_SUBHEADER_GC_COINS,
	ITEMSHOP_SUBHEADER_GC_CLEAR,
	ITEMSHOP_SUBHEADER_GC_OPEN,
	ITEMSHOP_SUBHEADER_GC_EDITOR,
	ITEMSHOP_SUBHEADER_GC_UPDATE,
	ITEMSHOP_SUBHEADER_GC_REFRESH,
	ITEMSHOP_SUBHEADER_GC_DELETE,
	ITEMSHOP_SUBHEADER_GC_NOT_ENOUGH_COINS,
	ITEMSHOP_SUBHEADER_GC_INVENTORY_FULL,
	ITEMSHOP_SUBHEADER_GC_WARP,
	ITEMSHOP_SUBHEADER_GC_NON_EDITOR,
	ITEMSHOP_SUBHEADER_GC_COUNT,
	ITEMSHOP_SUBHEADER_GC_UNKNOWN_ERROR,

};

typedef struct item_shop_packet
{
	BYTE	header;
	WORD	size;
	BYTE	subheader;
} TPacketGCItemShop;

typedef struct item_shop_coins_packet
{
	DWORD	coins;
} TPacketGCItemShopCoins;

typedef struct item_shop_delete_item
{
	DWORD	id;
	DWORD	category;
} TPacketGCItemShopDeleteItem;

typedef struct item_shop_buy
{
	BYTE	bHeader;
	DWORD	id;
	DWORD	category;
	BYTE	count;
} TPacketCGItemShopBuy;

typedef struct item_shop_add
{
	BYTE	bHeader;
	TItemShopItem	aItemShopItem;
	BYTE	bFlag;
} TPacketCGItemShopAddItem;

#endif