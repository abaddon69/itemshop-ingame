// search for:
#ifdef __PET_SYSTEM__
	private:
		bool m_bIsPet;
	public:
		void SetPet() { m_bIsPet = true; }
		bool IsPet() { return m_bIsPet; }
#endif

// add under:
#ifdef __ITEM_SHOP__
	public:
		void				LoadCoins(int coins)	{ m_iCoins = coins; }
		int					GetCoins()			{ return m_iCoins; }
		void				UpdateCoins(int coins);

	protected:
		int					m_iCoins;
		
#endif