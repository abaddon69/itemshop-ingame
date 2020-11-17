// skip if you use Great's offlineshop
// search for:
		CItemData *		MakeItemData(DWORD dwIndex);

// add under:
#ifdef ENABLE_ITEMSHOP
		TItemMap		GetItems() const { return m_ItemMap; }
#endif