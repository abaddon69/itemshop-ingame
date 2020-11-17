// search for:
#include "DragonSoul.h"

// add under:
#ifdef __ITEM_SHOP__
#include "itemshop_manager.h"
#endif

// search for:
void CInputMain::Refine(LPCHARACTER ch, const char* c_pData)
{
	[...]
}

// add under:
#ifdef __ITEM_SHOP__
void CInputMain::ItemShop(LPCHARACTER ch, BYTE header, const char* c_pData)
{
	switch(header)
	{
		case HEADER_CG_ITEMSHOP_OPEN:
		{
			if (!ch->CanWarp())
			{
				CItemShopManager::instance().ClientPacket(ITEMSHOP_SUBHEADER_GC_WARP, NULL, 0, ch);
				return;
			}
			CItemShopManager::instance().OpenItemShop(ch);
		}
			break;
		case HEADER_CG_ITEMSHOP_BUY:
		{
			if (!ch->CanWarp())
			{
				CItemShopManager::instance().ClientPacket(ITEMSHOP_SUBHEADER_GC_WARP, NULL, 0, ch);
				return;
			}
			
			TPacketCGItemShopBuy* p = (TPacketCGItemShopBuy*)c_pData;
			CItemShopManager::instance().BuyItem(ch, p->id, p->category, p->count);
		}
			break;

		case HEADER_CG_ITEMSHOP_ADD:
		{
			if (!ch->CanWarp())
			{
				CItemShopManager::instance().ClientPacket(ITEMSHOP_SUBHEADER_GC_WARP, NULL, 0, ch);
				return;
			}
			
			TPacketCGItemShopAddItem* p = (TPacketCGItemShopAddItem*)c_pData;
			CItemShopManager::instance().ManageItem(ch, p->bFlag, p->aItemShopItem);
		}
			break;
	}
}
#endif

// search for:
		case HEADER_CG_DRAGON_SOUL_REFINE:
			{
				[...]
			}

			break;

// add under:
#ifdef __ITEM_SHOP__
		case HEADER_CG_ITEMSHOP_OPEN:
		case HEADER_CG_ITEMSHOP_BUY:
		case HEADER_CG_ITEMSHOP_ADD:
			ItemShop(ch, bHeader, c_pData);
			break;
#endif