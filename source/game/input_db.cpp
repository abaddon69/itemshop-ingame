// search for:
#include "HackShield.h"

// add under:
#ifdef __ITEM_SHOP__
#include "itemshop_manager.h"
#endif

// search for:
#ifdef __AUCTION__
	case HEADER_DG_AUCTION_RESULT:
		if (auction_server)
			AuctionManager::instance().recv_result_auction(m_dwHandle, (TPacketDGResultAuction*)c_pData);
		break;
#endif

// add under:
#ifdef __ITEM_SHOP__
	case HEADER_DG_ITEMSHOP_COINS_LOAD:
		ItemShopCoinsLoad(DESC_MANAGER::instance().FindByHandle(m_dwHandle), c_pData);
		break;

	case HEADER_DG_ITEMSHOP_ITEMS_LOAD:
		ItemShopItemsLoad(DESC_MANAGER::instance().FindByHandle(m_dwHandle), c_pData);
		break;

	case HEADER_DG_ITEMSHOP_EDITORS_LOAD:
		ItemShopEditorsLoad(DESC_MANAGER::instance().FindByHandle(m_dwHandle), c_pData);
		break;

	case HEADER_DG_ITEMSHOP_ITEM_ADD:
		ItemShopItemAdd(DESC_MANAGER::instance().FindByHandle(m_dwHandle), c_pData);
		break;
#endif

// search for:
void CInputDB::RespondChannelStatus(LPDESC desc, const char* pcData) 
{
	[...]
}

// add under:
#ifdef __ITEM_SHOP__
void CInputDB::ItemShopCoinsLoad(LPDESC d, const char * c_pData)
{
	if (!d)
		return;

	if (!d->GetCharacter())
		return;

	LPCHARACTER ch = d->GetCharacter();

	DWORD coins = decode_4bytes(c_pData);
	c_pData += sizeof(DWORD);

	ch->LoadCoins(coins);
	sys_log(0, "Load Coins from db success! Recived data %d", coins);
}

void CInputDB::ItemShopItemsLoad(LPDESC d, const char * c_pData)
{
	DWORD dwCount = decode_4bytes(c_pData);
	c_pData += sizeof(DWORD);

	CItemShopManager::instance().LoadItems(dwCount, (TItemShopItem *) c_pData);
}

void CInputDB::ItemShopEditorsLoad(LPDESC d, const char * c_pData)
{	
	DWORD dwCount = decode_4bytes(c_pData);
	c_pData += sizeof(DWORD);

	CItemShopManager::instance().LoadEditors(dwCount, (TItemShopEditor *) c_pData);
}

void CInputDB::ItemShopItemAdd(LPDESC d, const char * c_pData)
{	
	BYTE bSuccess = decode_byte(c_pData);
	c_pData += sizeof(BYTE);

	BYTE bFlag = decode_byte(c_pData);
	c_pData += sizeof(BYTE);

	DWORD dwID = decode_4bytes(c_pData);
	c_pData += sizeof(DWORD);
	
	DWORD dwCategory = decode_4bytes(c_pData);
	c_pData += sizeof(DWORD);
	
	CItemShopManager::instance().AddItem(bSuccess, bFlag, dwID, dwCategory);

}
#endif