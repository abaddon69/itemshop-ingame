// search for:
long FN_get_apply_type(const char *apply_type_string)
{
	[...]
}

// add under:
#ifdef __ITEM_SHOP__
TItemShopTime aItemShopTime[ITEMSHOP_TIME_MAX_NUM + 1] = 
{
	// time, add to normal price
	{ 1 * 60,      10      },
	{ 2 * 60,      50      },
	{ 3 * 60,      100     },
	{ 4 * 60,      200     },
	{ 5 * 60,      500     },
	{ 6 * 60,      1000    },
};
#endif