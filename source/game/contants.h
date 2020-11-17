// search for:
long FN_get_apply_type(const char *apply_type_string);

// add under:
#ifdef __ITEM_SHOP__

enum
{
	ITEMSHOP_TIME_MAX_NUM = 6
};

typedef struct TItemShopTime
{
	DWORD	dwTime;
	DWORD	dwPrice;
} TItemShopTime;

extern TItemShopTime aItemShopTime[ITEMSHOP_TIME_MAX_NUM + 1];

#endif