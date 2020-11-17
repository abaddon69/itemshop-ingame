// search for:
#include "MovieMan.h"

// add under:
#ifdef ENABLE_ITEMSHOP
#include "PythonItemShop.h"
#endif

// search for:
		DWORD						m_dwHeight;

// add under:
#ifdef ENABLE_ITEMSHOP
		CItemShop					m_pyItemShop;
#endif