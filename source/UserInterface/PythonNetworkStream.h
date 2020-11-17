// search for:
		void __BettingGuildWar_SetBettingMoney(UINT uBettingMoney);

// add under:
#ifdef ENABLE_ITEMSHOP
	public:
		bool SendItemShopOpenPacket();
		bool SendItemShopBuyPacket(DWORD id, DWORD category, BYTE count);
		bool SendItemShopAddItemPacket(TItemShopItem item, BYTE flag);
	protected:
		bool RecvItemShopPacket();
#endif