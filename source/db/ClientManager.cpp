// search for:
#ifdef __AUCTION__
			case HEADER_GD_COMMAND_AUCTION:
			{
				[...]
			}
			break;
#endif

// add under:
#ifdef __ITEM_SHOP__
			case HEADER_GD_ITEMSHOP_ITEMS_REQUEST:
				QUERY_ITEMSHOP_ITEMS_LOAD(peer, dwHandle);
				break;
				
			case HEADER_GD_ITEMSHOP_EDITORS_REQUEST:
				QUERY_ITEMSHOP_EDITORS_LOAD(peer, dwHandle);
				break;
				
			case HEADER_GD_ITEMSHOP_UPDATE_COINS:
				QUERY_ITEMSHOP_UPDATE_COINS((TItemShopSetCoins *) data);
				break;
				
			case HEADER_GD_ITEMSHOP_ITEM_DELETE:
				QUERY_ITEMSHOP_DELETE_ITEM((TItemShopDeleteItem *) data);
				break;
				
			case HEADER_GD_ITEMSHOP_ITEM_ADD:
				QUERY_ITEMSHOP_ITEM_ADD(peer,(TItemShopEdit *) data);
				break;
#endif

// search for:
		case QID_AFFECT:

// add under:
#ifdef __ITEM_SHOP__
		case QID_ITEMSHOP_COINS_LOAD:
#endif

// search for:
			// MYSHOP_PRICE_LIST
		case QID_ITEMPRICE_LOAD:
			RESULT_PRICELIST_LOAD(peer, msg);
			break;
			// END_OF_MYSHOP_PRICE_LIST

// add under:
#ifdef __ITEM_SHOP__
		case QID_ITEMSHOP_ITEMS_LOAD:
			sys_log(0, "QUERY_RESULT: QID_ITEMSHOP_ITEMS_LOAD %p", msg);
			RESULT_ITEMSHOP_ITEMS_LOAD(peer, msg);
			break;
			
		case QID_ITEMSHOP_EDITORS_LOAD:
			sys_log(0, "QUERY_RESULT: QID_ITEMSHOP_EDITORS_LOAD %p", msg);
			RESULT_ITEMSHOP_EDITORS_LOAD(peer, msg);
			break;
#endif

// search for:
void CClientManager::RequestChannelStatus(CPeer* peer, DWORD dwHandle)
{
	[...]
}

// add under:
#ifdef __ITEM_SHOP__
void CClientManager::QUERY_ITEMSHOP_ITEMS_LOAD(CPeer * pkPeer, DWORD dwHandle)
{
	char szQuery[QUERY_MAX_LEN];
	snprintf(szQuery, sizeof(szQuery), "SELECT vnum, count, price, category, id, fixed_count, socket0,socket1,socket2,attrtype0,attrvalue0,attrtype1,attrvalue1,attrtype2,attrvalue2,attrtype3,attrvalue3,attrtype4,attrvalue4,attrtype5,attrvalue5,attrtype6,attrvalue6 FROM itemshop_items%s", GetTablePostfix());
	
	CDBManager::instance().ReturnQuery(szQuery, QID_ITEMSHOP_ITEMS_LOAD, pkPeer->GetHandle(), NULL);
}

void CClientManager::RESULT_ITEMSHOP_ITEMS_LOAD(CPeer * pkPeer, SQLMsg * msg)
{
	int iNumRows;
	
	MYSQL_RES * pRes = msg->Get()->pSQLResult;

	if ((iNumRows = mysql_num_rows(pRes)) == 0) // 데이터 없음
		return;

	static std::vector<TItemShopItem> s_elements;
	s_elements.resize(iNumRows);

	MYSQL_ROW row;

	for (int i = 0; i < iNumRows; ++i)
	{
		TItemShopItem & r = s_elements[i];
		row = mysql_fetch_row(pRes);
		
		int cur = 0;


		str_to_number(r.vnum, row[cur++]);
		str_to_number(r.count, row[cur++]);
		str_to_number(r.price, row[cur++]);
		str_to_number(r.category, row[cur++]);
		str_to_number(r.id, row[cur++]);
		str_to_number(r.fixed_count, row[cur++]);
		
		str_to_number(r.alSockets[0], row[cur++]);
		str_to_number(r.alSockets[1], row[cur++]);
		str_to_number(r.alSockets[2], row[cur++]);

		for (int j = 0; j < ITEM_ATTRIBUTE_MAX_NUM; j++)
		{
			str_to_number(r.aAttr[j].bType, row[cur++]);
			str_to_number(r.aAttr[j].sValue, row[cur++]);
		}
		
		
		sys_log(0, "RESULT_ITEMSHOP_ITEMS_LOAD: vnum [%d], count [%d], price [%d], category [%d], id [%d] ", r.vnum, r.count, r.price, r.category, r.id);
	}

	sys_log(0, "RESULT_ITEMSHOP_ITEMS_LOAD: finished with %d items", s_elements.size());

	DWORD dwCount = s_elements.size();

	pkPeer->EncodeHeader(HEADER_DG_ITEMSHOP_ITEMS_LOAD, 0, + sizeof(DWORD) + sizeof(TItemShopItem) * dwCount);
	pkPeer->Encode(&dwCount, sizeof(DWORD));
	pkPeer->Encode(&s_elements[0], sizeof(TItemShopItem) * dwCount);

}

void CClientManager::QUERY_ITEMSHOP_EDITORS_LOAD(CPeer * pkPeer, DWORD dwHandle)
{
	char szQuery[QUERY_MAX_LEN];
	snprintf(szQuery, sizeof(szQuery), "SELECT name FROM itemshop_editors%s", GetTablePostfix());
	
	CDBManager::instance().ReturnQuery(szQuery, QID_ITEMSHOP_EDITORS_LOAD, pkPeer->GetHandle(), NULL);
}

void CClientManager::RESULT_ITEMSHOP_EDITORS_LOAD(CPeer * pkPeer, SQLMsg * msg)
{
	int iNumRows;
	
	MYSQL_RES * pRes = msg->Get()->pSQLResult;

	if ((iNumRows = mysql_num_rows(pRes)) == 0) // 데이터 없음
		return;

	static std::vector<TItemShopEditor> s_elements;
	s_elements.resize(iNumRows);

	MYSQL_ROW row;

	for (int i = 0; i < iNumRows; ++i)
	{
		TItemShopEditor & r = s_elements[i];
		row = mysql_fetch_row(pRes);

		strcpy(r.name, row[0]);
		
		sys_log(0, "RESULT_ITEMSHOP_EDITORS_LOAD: name [%s]", r.name);
	}

	sys_log(0, "RESULT_ITEMSHOP_EDITORS_LOAD: finished with %d items", s_elements.size());

	DWORD dwCount = s_elements.size();

	pkPeer->EncodeHeader(HEADER_DG_ITEMSHOP_EDITORS_LOAD, 0, sizeof(DWORD) + sizeof(TItemShopEditor) * dwCount);
	pkPeer->Encode(&dwCount, sizeof(DWORD));
	pkPeer->Encode(&s_elements[0], sizeof(TItemShopEditor) * dwCount);
}

void CClientManager::QUERY_ITEMSHOP_UPDATE_COINS(TItemShopSetCoins * p)
{
	char queryStr[QUERY_MAX_LEN];

	snprintf(queryStr, sizeof(queryStr),
			"UPDATE %saccount%s SET coins = coins-%d WHERE id=%d",
			GetAccountDBName(), GetTablePostfix(), p->coins, p->account_id);

	CDBManager::instance().AsyncQuery(queryStr);
}

void CClientManager::QUERY_ITEMSHOP_DELETE_ITEM(TItemShopDeleteItem * p)
{
	char queryStr[QUERY_MAX_LEN];

	snprintf(queryStr, sizeof(queryStr),
			"DELETE from itemshop_items%s WHERE id=%d AND category=%d",
			GetTablePostfix(), p->id, p->category);

	CDBManager::instance().AsyncQuery(queryStr);
}

void CClientManager::QUERY_ITEMSHOP_ITEM_ADD(CPeer * pkPeer, TItemShopEdit * p)
{
	TItemShopItem item = p->item;
	
	char queryStr[QUERY_MAX_LEN];
	
	int id = (p->flag == ITEMSHOP_ITEM_FLAG_EDIT) ? item.id : 0;

	snprintf(queryStr, sizeof(queryStr),
			"REPLACE INTO itemshop_items%s "
			
			"(id, category, vnum, price, count,"
			" socket0,socket1,socket2,"
			"attrtype0,attrvalue0,attrtype1,attrvalue1,attrtype2,attrvalue2,attrtype3,attrvalue3,attrtype4,attrvalue4,attrtype5,attrvalue5,attrtype6,attrvalue6,"
			"fixed_count)"
			
			"VALUES (%d, %d, %d, %d, %d, "
			"%d, %d, %d, "
			"%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, "
			"%d)",
			GetTablePostfix(), id, item.category, item.vnum, item.price, item.count,
			
			item.alSockets[0], item.alSockets[1], item.alSockets[2],
			
			item.aAttr[0].bType, item.aAttr[0].sValue,
			item.aAttr[1].bType, item.aAttr[1].sValue,
			item.aAttr[2].bType, item.aAttr[2].sValue,
			item.aAttr[3].bType, item.aAttr[3].sValue,
			item.aAttr[4].bType, item.aAttr[4].sValue,
			item.aAttr[5].bType, item.aAttr[5].sValue,
			item.aAttr[6].bType, item.aAttr[6].sValue,
			
			item.fixed_count
	);

	std::unique_ptr<SQLMsg> pMsg(CDBManager::instance().DirectQuery(queryStr));

	BYTE bSuccess = (pMsg->Get()->uiAffectedRows > 0);
	BYTE bFlag = p->flag;
	DWORD dwID = (bSuccess && bFlag == ITEMSHOP_ITEM_FLAG_ADD)? pMsg->Get()->uiInsertID : p->item.id;
	DWORD dwCategory	= p->item.category;

	pkPeer->EncodeHeader(HEADER_DG_ITEMSHOP_ITEM_ADD, 0, sizeof(BYTE) + sizeof(BYTE) + sizeof(DWORD) + sizeof(DWORD));
	pkPeer->Encode(&bSuccess, sizeof(BYTE));
	pkPeer->Encode(&bFlag, sizeof(BYTE));
	pkPeer->Encode(&dwID, sizeof(DWORD));
	pkPeer->Encode(&dwCategory, sizeof(DWORD));
}
#endif