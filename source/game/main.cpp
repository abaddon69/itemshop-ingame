// search for:
#ifdef __AUCTION__
#include "auction_manager.h"
#endif

// add under:
#ifdef __ITEM_SHOP__
#include "itemshop_manager.h"
#endif

// search for:
#ifdef __AUCTION__
	AuctionManager auctionManager;
#endif

// add under:
#ifdef __ITEM_SHOP__
	CItemShopManager itemshop_manager;
#endif

// search for:
	PanamaLoad();

// add under:
#ifdef __ITEM_SHOP__
	CItemShopManager::instance().Initialize();
#endif