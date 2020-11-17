// search for:
#include "ProcessCRC.h"

// add under:
#ifdef ENABLE_ITEMSHOP
#include "PythonItemShop.h"
#endif

// search for:
			case HEADER_GC_DRAGON_SOUL_REFINE:
				ret = RecvDragonSoulRefine();
				break;

// add under:
#ifdef ENABLE_ITEMSHOP
			case HEADER_GC_ITEMSHOP:
				ret = RecvItemShopPacket();
#endif

// search for:
bool CPythonNetworkStream::SendDragonSoulRefinePacket(BYTE bRefineType, TItemPos* pos)
{
	[...]
}

// add under:
#ifdef ENABLE_ITEMSHOP
bool CPythonNetworkStream::RecvItemShopPacket()
{
	TPacketGCItemShop kItemShop;
	if (!Recv(sizeof(kItemShop), &kItemShop))
		return false;

	switch (kItemShop.subheader)
	{
	case ITEMSHOP_SUBHEADER_GC_ITEM:
	{
									   TItemShopItem item_packet;
									   if (!Recv(sizeof(TItemShopItem), &item_packet))
										   return false;

									   CItemShop::Instance().SetItemData(item_packet);
									   break;

	}
		

	case ITEMSHOP_SUBHEADER_GC_COINS:
	{
										TPacketGCItemShopCoins packet;
										if (!Recv(sizeof(TPacketGCItemShopCoins), &packet))
											return false;

										CItemShop::Instance().SetCoins(packet.coins);
										break;
	}

	case ITEMSHOP_SUBHEADER_GC_CLEAR:
	{
										CItemShop::Instance().ClearItems();
										break;
	}

	case ITEMSHOP_SUBHEADER_GC_OPEN:
	{
									   PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_ItemShopOpen", Py_BuildValue("()"));
									   break;
	}

	case ITEMSHOP_SUBHEADER_GC_EDITOR:
	{
										 BYTE flag;
										 if (!Recv(sizeof(BYTE), &flag))
											 return false;

										 if (flag)
											PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_ItemShopSetEditorFlag", Py_BuildValue("(b)", true));
										 else
											 PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_ItemShopSetEditorFlag", Py_BuildValue("(b)", false));
										 break;
	}

	case ITEMSHOP_SUBHEADER_GC_UPDATE:
	{
										 TItemShopItem item_packet;
										 if (!Recv(sizeof(TItemShopItem), &item_packet))
											 return false;


										 CItemShop::Instance().UpdateItem(item_packet);
										 break;
	}

	case ITEMSHOP_SUBHEADER_GC_DELETE:
	{
										 TPacketGCItemShopDeleteItem packet;
										 if (!Recv(sizeof(TPacketGCItemShopDeleteItem), &packet))
											 return false;

										 CItemShop::Instance().DelItemData(packet.id, packet.category);
										 break;
	}

	case ITEMSHOP_SUBHEADER_GC_REFRESH:
	{
										PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "BINARY_ItemShopRefresh", Py_BuildValue("()"));
										break;
	}

	case ITEMSHOP_SUBHEADER_GC_NOT_ENOUGH_COINS:
	{
										PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnItemShopError", Py_BuildValue("(s)", "NOT_ENOUGH_COINS"));
										break;
	}

	case ITEMSHOP_SUBHEADER_GC_INVENTORY_FULL:
	{
										PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnItemShopError", Py_BuildValue("(s)", "INVENTORY_FULL"));
										break;
	}

	case ITEMSHOP_SUBHEADER_GC_WARP:
	{
										PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnItemShopError", Py_BuildValue("(s)", "WARP"));
										break;
	}

	case ITEMSHOP_SUBHEADER_GC_NON_EDITOR:
	{
										PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnItemShopError", Py_BuildValue("(s)", "NOT_EDITOR"));
										break;
	}

	case ITEMSHOP_SUBHEADER_GC_COUNT:
	{
										PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnItemShopError", Py_BuildValue("(s)", "COUNT"));
										break;
	}

	case ITEMSHOP_SUBHEADER_GC_UNKNOWN_ERROR:
	{
										PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "OnItemShopError", Py_BuildValue("(s)", "UNKNOWN_ERROR"));
										break;
	}

	default:
		break;

	}


	
	return true;
}

bool CPythonNetworkStream::SendItemShopOpenPacket()
{
	BYTE bHeader = HEADER_CG_ITEMSHOP_OPEN;
	if (!Send(sizeof(BYTE), &bHeader))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendItemShopBuyPacket(DWORD id, DWORD category, BYTE count)
{
	TPacketCGItemShopBuy kItemShopBuy;
	kItemShopBuy.bHeader = HEADER_CG_ITEMSHOP_BUY;
	kItemShopBuy.id = id;
	kItemShopBuy.category = category;
	kItemShopBuy.count = count;
	if (!Send(sizeof(kItemShopBuy), &kItemShopBuy))
		return false;

	return SendSequence();
}

bool CPythonNetworkStream::SendItemShopAddItemPacket(TItemShopItem item, BYTE flag)
{
	TPacketCGItemShopAddItem kItemShopAdd;
	kItemShopAdd.bHeader = HEADER_CG_ITEMSHOP_ADD;
	kItemShopAdd.aItemShopItem = item;
	kItemShopAdd.bFlag = flag;

	if (!Send(sizeof(kItemShopAdd), &kItemShopAdd))
		return false;

	return SendSequence();
}

#endif