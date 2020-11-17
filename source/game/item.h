## search for:
	private :
		void		SetAttribute(int i, BYTE bType, short sValue);

## replace it with:
#ifdef __ITEM_SHOP__
	public :
		void		SetAttribute(int i, BYTE bType, short sValue);
#else
	private :
		void		SetAttribute(int i, BYTE bType, short sValue);
#endif