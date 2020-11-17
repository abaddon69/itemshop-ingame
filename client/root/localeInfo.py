## search for:
STAT_MINUS_DESCRIPTION = {
	[...]
}

## add under:
ITEMSHOP_ERROR_DICT = {
	"NOT_ENOUGH_COINS" : ITEMSHOP_NOT_ENOUGH_COINS,
	"INVENTORY_FULL" : ITEMSHOP_INVENTORY_FULL,
	"WARP" : ITEMSHOP_WARP,
	"NOT_EDITOR" : ITEMSHOP_NON_EDITOR,
	"COUNT" : ITEMSHOP_COUNT,
	"UNKNOWN_ERROR" : ITEMSHOP_UNKNOWN_ERROR,
}

## add at the end of the file:
def ITEMSHOP_DO_YOU_BUY_ITEM(buyItemName, buyItemCount, buyItemPrice) :
	if buyItemCount > 1 :
		return ITEMSHOP_DO_YOU_BUY_ITEM2 % ( buyItemName, buyItemCount, buyItemPrice )
	else:
		return ITEMSHOP_DO_YOU_BUY_ITEM1 % ( buyItemName, buyItemPrice )