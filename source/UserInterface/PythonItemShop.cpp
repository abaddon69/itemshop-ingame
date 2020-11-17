#include "StdAfx.h"
#include "PythonItemShop.h"

#include "PythonNetworkStream.h"

#ifdef ENABLE_ITEMSHOP

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

void CItemShop::ClearItems()
{
	m_ItemInstanceVector.clear();
}

void CItemShop::SetItemData(TItemShopItem item)
{
	m_ItemInstanceVector.push_back(item);
}

void CItemShop::DelItemData(DWORD dwSlotIndex, DWORD dwCategoryIndex)
{

	for (DWORD i = 0; i < m_ItemInstanceVector.size(); ++i)
		if (m_ItemInstanceVector[i].id == dwSlotIndex && m_ItemInstanceVector[i].category == dwCategoryIndex)
			m_ItemInstanceVector.erase(m_ItemInstanceVector.begin() + i);
}

void CItemShop::UpdateItem(TItemShopItem pkItem)
{
	for (DWORD i = 0; i < m_ItemInstanceVector.size(); ++i)
		if (m_ItemInstanceVector[i].id == pkItem.id && m_ItemInstanceVector[i].category == pkItem.category)
			m_ItemInstanceVector[i] = pkItem;
}

TItemShopItem CItemShop::GetItemDataPtr(DWORD dwSlotIndex, DWORD dwCategoryIndex)
{
	for (auto it = m_ItemInstanceVector.begin(); it != m_ItemInstanceVector.end(); ++it)
	{
		TItemShopItem item = *(it);

		if (item.id == dwSlotIndex && item.category == dwCategoryIndex)
		{
			return item;
		}
	}
}

std::vector<int> CItemShop::GetCategoryItemPos(DWORD dwCategoryIndex)
{
	std::vector<int> temp_items;

	auto it = m_ItemInstanceVector.begin();
	while (it != m_ItemInstanceVector.end())
	{
		TItemShopItem item = *(it++);

		if (item.category == dwCategoryIndex)
			temp_items.push_back(item.id);
	}

	return temp_items;
}

CItemShop::CItemShop()
{
}

CItemShop::~CItemShop()
{
}

PyObject * itemshopGetItemVnum(PyObject * poSelf, PyObject * poArgs)
{
	int ipos;
	if (!PyTuple_GetInteger(poArgs, 0, &ipos))
		return Py_BadArgument();

	int icategory;
	if (!PyTuple_GetInteger(poArgs, 1, &icategory))
		return Py_BadArgument();

	TItemShopItem pInstance = CItemShop::Instance().GetItemDataPtr(ipos, icategory);
	if (&pInstance == nullptr)
		return Py_BuildException();

	return Py_BuildValue("i", pInstance.vnum);
}

PyObject * itemshopGetCategoryItems(PyObject * poSelf, PyObject * poArgs)
{
	int icategory;
	if (!PyTuple_GetInteger(poArgs, 0, &icategory))
		return Py_BadArgument();

	std::vector<int> m_vec_items = CItemShop::Instance().GetCategoryItemPos(icategory);

	PyObject * tuple = PyTuple_New((Py_ssize_t) m_vec_items.size());

	for (int i = 0; i < m_vec_items.size(); i++)
	{
		PyTuple_SetItem(tuple, i, Py_BuildValue("i", m_vec_items[i]));
	}

	return tuple;
}

PyObject * itemshopGetItemCount(PyObject * poSelf, PyObject * poArgs)
{
	int ipos;
	if (!PyTuple_GetInteger(poArgs, 0, &ipos))
		return Py_BadArgument();

	int icategory;
	if (!PyTuple_GetInteger(poArgs, 1, &icategory))
		return Py_BadArgument();

	TItemShopItem pInstance = CItemShop::Instance().GetItemDataPtr(ipos, icategory);
	if (&pInstance == nullptr)
		return Py_BuildException();

	return Py_BuildValue("i", pInstance.count);
}

PyObject * itemshopGetItemMetinSocket(PyObject * poSelf, PyObject * poArgs)
{
	int iSlotIndex;
	if (!PyTuple_GetInteger(poArgs, 0, &iSlotIndex))
		return Py_BadArgument();

	int icategory;
	if (!PyTuple_GetInteger(poArgs, 1, &icategory))
		return Py_BadArgument();

	int iSocketIndex;
	if (!PyTuple_GetInteger(poArgs, 2, &iSocketIndex))
		return Py_BadArgument();

	if (iSocketIndex >= ITEM_SOCKET_SLOT_MAX_NUM)
		return Py_BuildException();

	TItemShopItem pInstance = CItemShop::Instance().GetItemDataPtr(iSlotIndex, icategory);
	if (&pInstance == nullptr)
		return Py_BuildException();

	return Py_BuildValue("i", pInstance.alSockets[iSocketIndex]);
}

PyObject * itemshopGetItemAttribute(PyObject * poSelf, PyObject * poArgs)
{
	int iSlotIndex;
	if (!PyTuple_GetInteger(poArgs, 0, &iSlotIndex))
		return Py_BuildException();

	int icategory;
	if (!PyTuple_GetInteger(poArgs, 1, &icategory))
		return Py_BadArgument();

	int iAttrSlotIndex;
	if (!PyTuple_GetInteger(poArgs, 2, &iAttrSlotIndex))
		return Py_BuildException();

	if (iAttrSlotIndex >= 0 && iAttrSlotIndex < ITEM_ATTRIBUTE_SLOT_MAX_NUM)
	{
		TItemShopItem pInstance = CItemShop::Instance().GetItemDataPtr(iSlotIndex, icategory);
		if (&pInstance)
			return Py_BuildValue("ii", pInstance.aAttr[iAttrSlotIndex].bType, pInstance.aAttr[iAttrSlotIndex].sValue);
	}

	return Py_BuildValue("ii", 0, 0);
}

PyObject * itemshopGetItemPrice(PyObject * poSelf, PyObject * poArgs)
{
	int ipos;
	if (!PyTuple_GetInteger(poArgs, 0, &ipos))
		return Py_BadArgument();

	int icategory;
	if (!PyTuple_GetInteger(poArgs, 1, &icategory))
		return Py_BadArgument();

	TItemShopItem pInstance = CItemShop::Instance().GetItemDataPtr(ipos, icategory);
	if (&pInstance == nullptr)
		return Py_BuildException();

	return Py_BuildValue("i", pInstance.price);
}

PyObject * itemshopGetCoins(PyObject * poSelf, PyObject * poArgs)
{
	
	return Py_BuildValue("i", CItemShop::Instance().GetCoins());
}

PyObject * itemshopIsFixedCount(PyObject * poSelf, PyObject * poArgs)
{
	int ipos;
	if (!PyTuple_GetInteger(poArgs, 0, &ipos))
		return Py_BadArgument();

	int icategory;
	if (!PyTuple_GetInteger(poArgs, 1, &icategory))
		return Py_BadArgument();

	TItemShopItem pInstance = CItemShop::Instance().GetItemDataPtr(ipos, icategory);
	if (&pInstance == nullptr)
		return Py_BuildException();

	return Py_BuildValue("i", pInstance.fixed_count);
}

PyObject * itemshopSendItemShopPacket(PyObject * poSelf, PyObject * poArgs)
{

	int ipos, icategory, ivnum, iprice, icount;
	BYTE bfixedcount, bflag;

	long alSockets[ITEM_SOCKET_SLOT_MAX_NUM];
	TPlayerItemAttribute aAttr[ITEM_ATTRIBUTE_SLOT_MAX_NUM];

	if (!PyTuple_GetInteger(poArgs, 0, &ipos))
		return Py_BadArgument();

	if (!PyTuple_GetInteger(poArgs, 1, &icategory))
		return Py_BadArgument();

	if (!PyTuple_GetInteger(poArgs, 2, &ivnum))
		return Py_BadArgument();

	if (!PyTuple_GetInteger(poArgs, 3, &iprice))
		return Py_BadArgument();

	if (!PyTuple_GetInteger(poArgs, 4, &icount))
		return Py_BadArgument();

	if (!PyTuple_GetByte(poArgs, 5, &bfixedcount))
		return Py_BadArgument();

	PyObject* poSocket = PyTuple_GetItem(poArgs, 6);
	if (!PyList_Check(poSocket))
		return Py_BadArgument();

	for (int i = 0; i < ITEM_SOCKET_SLOT_MAX_NUM; i++)
	{
		alSockets[i] = PyInt_AsLong(PyList_GetItem(poSocket, i));
	}

	PyObject* poAttr = PyTuple_GetItem(poArgs, 7);
	if (!PyList_Check(poAttr))
		return Py_BadArgument();

	for (int i = 0; i < ITEM_ATTRIBUTE_SLOT_MAX_NUM; i++)
	{
		PyObject* poTempAttr = PyList_GetItem(poAttr, i);
		if (!poTempAttr)
		{
			aAttr[i].bType = 0;
			aAttr[i].sValue = 0;

			continue;
		}

		aAttr[i].bType = PyInt_AsLong(PyList_GetItem(poTempAttr, 0));
		aAttr[i].sValue = PyInt_AsLong(PyList_GetItem(poTempAttr, 1));
	}

	if (!PyTuple_GetByte(poArgs, 8, &bflag))
		return Py_BadArgument();

	TItemShopItem aItemShopItem;
	aItemShopItem.id = ipos;
	aItemShopItem.category = icategory;
	aItemShopItem.vnum = ivnum;
	aItemShopItem.count = icount;
	aItemShopItem.price = iprice;
	aItemShopItem.fixed_count = bfixedcount;

	memcpy(aItemShopItem.alSockets, alSockets, sizeof(alSockets));
	memcpy(aItemShopItem.aAttr, aAttr, sizeof(aAttr));

	CPythonNetworkStream& rns = CPythonNetworkStream::Instance();
	rns.SendItemShopAddItemPacket(aItemShopItem, bflag);

	return Py_BuildNone();
}

 
void inititemshop()
{
	static PyMethodDef s_methods[] =
	{
		// clientData
		{ "GetItemID", itemshopGetItemVnum, METH_VARARGS },
		{ "GetCategoryItemPos", itemshopGetCategoryItems, METH_VARARGS },
		{ "GetItemCount", itemshopGetItemCount, METH_VARARGS },
		{ "GetItemPrice", itemshopGetItemPrice, METH_VARARGS },
		{ "GetItemMetinSocket", itemshopGetItemMetinSocket, METH_VARARGS },
		{ "GetItemAttribute", itemshopGetItemAttribute, METH_VARARGS },
		{ "GetCoins", itemshopGetCoins, METH_VARARGS },
		{ "IsFixedCount", itemshopIsFixedCount, METH_VARARGS },

		// serverCommands

		{ "SendItemShopPacket", itemshopSendItemShopPacket, METH_VARARGS },

		{ NULL, NULL, NULL },
	};

	PyObject * poModule = Py_InitModule("itemshop", s_methods);

	PyModule_AddIntConstant(poModule, "EDITOR_FLAG_ADD",	EDITOR_FLAG_ADD);
	PyModule_AddIntConstant(poModule, "EDITOR_FLAG_EDIT",	EDITOR_FLAG_EDIT);
	PyModule_AddIntConstant(poModule, "EDITOR_FLAG_DELETE", EDITOR_FLAG_DELETE);	

	PyModule_AddIntConstant(poModule, "ITEMSHOP_TIME_MAX_NUM", ITEMSHOP_TIME_MAX_NUM);
	
	for (int i = 0; i < ITEMSHOP_TIME_MAX_NUM + 1; i++)
	{
		char szTime[16 + 1];
		snprintf(szTime, sizeof(szTime), "TIME_%02d", i);
		PyModule_AddIntConstant(poModule, szTime, aItemShopTime[i].dwTime);		
		
		char szPrice[16 + 1];
		snprintf(szPrice, sizeof(szPrice), "PRICE_%02d", i);
		PyModule_AddIntConstant(poModule, szPrice, aItemShopTime[i].dwPrice);
	}

}

#endif