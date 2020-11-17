// search for:
#ifdef __PET_SYSTEM__
#include "PetSystem.h"
#endif

// add under:
#ifdef __ITEM_SHOP__
#include "itemshop_manager.h"
#endif

// search for:
	sys_log(0, "DISCONNECT: %s (%s)", GetName(), c_pszReason ? c_pszReason : "unset" );

// add under:
#ifdef __ITEM_SHOP__
	CItemShopManager::instance().RemoveViewer(this);
#endif

// add at the end of the file
#ifdef __ITEM_SHOP__
void CHARACTER::UpdateCoins(int coins)
{
	TItemShopSetCoins p;
	p.coins = coins;
	p.account_id = GetDesc()->GetAccountTable().id;
	db_clientdesc->DBPacket(HEADER_GD_ITEMSHOP_UPDATE_COINS, 0, &p, sizeof(TItemShopSetCoins));
	m_iCoins -= coins;
}
#endif