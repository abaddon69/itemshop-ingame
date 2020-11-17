// search for:
	HEADER_GD_REQUEST_CHANNELSTATUS	= 140,

// add under:
#ifdef __ITEM_SHOP__
	HEADER_GD_ITEMSHOP_ITEMS_REQUEST = 141,
	HEADER_GD_ITEMSHOP_UPDATE_COINS = 142,
	HEADER_GD_ITEMSHOP_ITEM_DELETE = 143,
	HEADER_GD_ITEMSHOP_ITEM_ADD = 144,
	HEADER_GD_ITEMSHOP_ITEM_EDIT = 145,
	HEADER_GD_ITEMSHOP_EDITORS_REQUEST = 146,
#endif

// search for:
	HEADER_DG_RESPOND_CHANNELSTATUS		= 181,

// add under:
#ifdef __ITEM_SHOP__
	HEADER_DG_ITEMSHOP_COINS_LOAD	= 182,
	HEADER_DG_ITEMSHOP_ITEMS_LOAD	= 183,
	HEADER_DG_ITEMSHOP_EDITORS_LOAD	= 184,
	HEADER_DG_ITEMSHOP_ITEM_ADD		= 188,
#endif

// search for:
typedef struct SChannelStatus
{
	[...]
} TChannelStatus;

// add under:
#ifdef __ITEM_SHOP__
typedef struct SItemShopItem
{
	DWORD	vnum;
	BYTE	count;
	DWORD	price;
	BYTE	category;
	DWORD	id;
	long	alSockets[ITEM_SOCKET_MAX_NUM];
	TPlayerItemAttribute	aAttr[ITEM_ATTRIBUTE_MAX_NUM];
	BYTE	fixed_count;
	
	SItemShopItem()
	
	{
		vnum = 0;
		price = 0;
		count = 0;
		category = 0;
		id = 0;
	}
	
} TItemShopItem;

typedef struct SItemShopSetCoins
{
	DWORD coins;
	DWORD account_id;
} TItemShopSetCoins;

typedef struct SItemShopDeleteItem
{
	DWORD id;
	DWORD category;
} TItemShopDeleteItem;

typedef struct SItemShopEditor
{
	char	name[CHARACTER_NAME_MAX_LEN+1];
}TItemShopEditor;

typedef struct SItemShopEdit
{
	BYTE flag;
	TItemShopItem item;
} TItemShopEdit;

#endif