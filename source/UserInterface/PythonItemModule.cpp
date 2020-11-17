// search for:
PyObject* itemLoadItemTable(PyObject* poSelf, PyObject* poArgs)
{
	char * szFileName;
	if (!PyTuple_GetString(poArgs, 0, &szFileName))
		return Py_BadArgument();

	CItemManager::Instance().LoadItemTable(szFileName);
	return Py_BuildNone();
}

// add under:
#ifdef ENABLE_ITEMSHOP
PyObject * itemGetWeaponSockets(PyObject * poSelf, PyObject * poArgs)
{
	CItemManager::TItemMap m_ItemMap = CItemManager::Instance().GetItems();
	CItemManager::TItemMap::iterator f = m_ItemMap.begin();
	std::vector<DWORD> m_SocketVec;
	int i = 0;
	while (m_ItemMap.end() != f)
	{
		if (f->second->GetType() == CItemData::ITEM_TYPE_METIN && f->second->GetWearFlags() == CItemData::WEARABLE_WEAPON)
			m_SocketVec.push_back(f->second->GetIndex());
		f++;
	}
	PyObject * tuple = PyTuple_New((Py_ssize_t)m_SocketVec.size());

	for (int i = 0; i < m_SocketVec.size(); i++)
	{
		PyTuple_SetItem(tuple, i, Py_BuildValue("i", m_SocketVec[i]));
	}
	return tuple;
}
PyObject * itemGetBodySockets(PyObject * poSelf, PyObject * poArgs)
{
	CItemManager::TItemMap m_ItemMap = CItemManager::Instance().GetItems();
	CItemManager::TItemMap::iterator f = m_ItemMap.begin();
	std::vector<DWORD> m_SocketVec;
	int i = 0;
	while (m_ItemMap.end() != f)
	{
		if (f->second->GetType() == CItemData::ITEM_TYPE_METIN && f->second->GetWearFlags() == CItemData::WEARABLE_BODY)
			m_SocketVec.push_back(f->second->GetIndex());
		f++;
	}
	PyObject * tuple = PyTuple_New((Py_ssize_t)m_SocketVec.size());

	for (int i = 0; i < m_SocketVec.size(); i++)
	{
		PyTuple_SetItem(tuple, i, Py_BuildValue("i", m_SocketVec[i]));
	}
	return tuple;
}

PyObject * itemGetItemNames(PyObject * poSelf, PyObject * poArgs)
{
	CItemManager::TItemMap m_ItemMap = CItemManager::Instance().GetItems();
	CItemManager::TItemMap::iterator f = m_ItemMap.begin();
	PyObject* dict = PyTuple_New(m_ItemMap.size());
	int i = 0;
	while (m_ItemMap.end() != f)
	{
		PyObject* item = PyDict_New();
		PyDict_SetItemString(item, "vnum", Py_BuildValue("i", f->second->GetIndex()));
		PyDict_SetItemString(item, "name", Py_BuildValue("s", f->second->GetName()));
		PyTuple_SetItem(dict, i++, item);
		f++;
	}
	return dict;
}
#endif

// search for:
		{ "LoadItemTable",					itemLoadItemTable,						METH_VARARGS },

// add under:
#ifdef ENABLE_ITEMSHOP
		{ "GetWeaponSockets",				itemGetWeaponSockets,					METH_VARARGS },
		{ "GetBodySockets",					itemGetBodySockets,						METH_VARARGS },
		{ "GetNames",						itemGetItemNames,						METH_VARARGS },
#endif