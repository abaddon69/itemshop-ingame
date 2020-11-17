#pragma once

#include "Packet.h"

enum EEditorFlag 
{
	EDITOR_FLAG_ADD,
	EDITOR_FLAG_EDIT,
	EDITOR_FLAG_DELETE
};

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

class CItemShop : public CSingleton<CItemShop>
{
public:
	CItemShop();
	virtual						~CItemShop();

	void						ClearItems();
	void						SetItemData(TItemShopItem item);
	void						DelItemData(DWORD dwSlotIndex, DWORD dwCategoryIndex);
	void						UpdateItem(TItemShopItem item);

	TItemShopItem				GetItemDataPtr(DWORD dwSlotIndex, DWORD dwCategoryIndex);
	std::vector<int>			GetCategoryItemPos(DWORD dwCategoryIndex);
	void						SetCoins(DWORD coins) { m_dwCoins = coins; }
	DWORD						GetCoins() { return m_dwCoins; }

protected:
	std::vector<TItemShopItem>	m_ItemInstanceVector;
	DWORD						m_dwCoins;
};