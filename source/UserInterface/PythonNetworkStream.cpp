// search for:
			Set(HEADER_GC_DRAGON_SOUL_REFINE,		CNetworkPacketHeaderMap::TPacketType(sizeof(TPacketGCDragonSoulRefine), STATIC_SIZE_PACKET));

// add under:
#ifdef ENABLE_ITEMSHOP
			Set(HEADER_GC_ITEMSHOP, CNetworkPacketHeaderMap::TPacketType(sizeof(TPacketGCItemShop), DYNAMIC_SIZE_PACKET));
#endif