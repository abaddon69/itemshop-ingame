// search for:
			// Affect
			snprintf(szQuery, sizeof(szQuery),
					"SELECT dwPID,bType,bApplyOn,lApplyValue,dwFlag,lDuration,lSPCost FROM affect%s WHERE dwPID=%d",
					GetTablePostfix(), pTab->id);
			CDBManager::instance().ReturnQuery(szQuery, QID_AFFECT, peer->GetHandle(), new ClientHandleInfo(dwHandle));

// add under:
#ifdef __ITEM_SHOP__
			// Item Shop
			snprintf(szQuery, sizeof(szQuery),
					"SELECT coins FROM %saccount%s WHERE id=%d",
					GetAccountDBName(), GetTablePostfix(), packet->account_id);
			CDBManager::instance().ReturnQuery(szQuery, QID_ITEMSHOP_COINS_LOAD, peer->GetHandle(), new ClientHandleInfo(dwHandle));
#endif

// search for:
			snprintf(szQuery, sizeof(szQuery), 
					"SELECT dwPID, bType, bApplyOn, lApplyValue, dwFlag, lDuration, lSPCost FROM affect%s WHERE dwPID=%d",
					GetTablePostfix(), pTab->id);

			CDBManager::instance().ReturnQuery(szQuery,
					QID_AFFECT,
					peer->GetHandle(),
					new ClientHandleInfo(dwHandle, pTab->id));

// add under:
#ifdef __ITEM_SHOP__
			snprintf(szQuery, sizeof(szQuery), 
					"SELECT coins FROM %saccount%s WHERE id=%d",
					GetAccountDBName(), GetTablePostfix(), packet->account_id);

			CDBManager::instance().ReturnQuery(szQuery,
					QID_ITEMSHOP_COINS_LOAD,
					peer->GetHandle(),
					new ClientHandleInfo(dwHandle, pTab->id));
#endif

// search for:
		snprintf(queryStr, sizeof(queryStr),
				"SELECT dwPID,bType,bApplyOn,lApplyValue,dwFlag,lDuration,lSPCost FROM affect%s WHERE dwPID=%d",
				GetTablePostfix(), packet->player_id);
		CDBManager::instance().ReturnQuery(queryStr, QID_AFFECT, peer->GetHandle(), new ClientHandleInfo(dwHandle, packet->player_id));

// add under:
#ifdef __ITEM_SHOP__
		snprintf(queryStr, sizeof(queryStr),
				"SELECT coins FROM %saccount%s WHERE id=%d",
				GetAccountDBName(), GetTablePostfix(), packet->account_id);
		CDBManager::instance().ReturnQuery(queryStr, QID_ITEMSHOP_COINS_LOAD, peer->GetHandle(), new ClientHandleInfo(dwHandle, packet->player_id));
#endif

// search for:
		case QID_AFFECT:
			sys_log(0, "QID_AFFECT %u", info->dwHandle);
			RESULT_AFFECT_LOAD(peer, pSQLResult, info->dwHandle);
			break;

// add under:
#ifdef __ITEM_SHOP__
		case QID_ITEMSHOP_COINS_LOAD:
			sys_log(0, "QID_ITEMSHOP_COINS_LOAD %u", info->dwHandle);
			RESULT_ITEMSHOP_COINS_LOAD(peer, pSQLResult, info->dwHandle);
			break;
#endif

// search for:
void CClientManager::FlushPlayerCacheSet(DWORD pid)
{
	[...]
}

// add under:
#ifdef __ITEM_SHOP__
void CClientManager::RESULT_ITEMSHOP_COINS_LOAD(CPeer * peer, MYSQL_RES * pRes, DWORD dwHandle)
{
	int iNumRows;

	if ((iNumRows = mysql_num_rows(pRes)) == 0) // 데이터 없음
		return;


	MYSQL_ROW row;

	row = mysql_fetch_row(pRes);
	DWORD coins = 0;
	str_to_number(coins, row[0]);

	sys_log(0, "ITEMSHOP_COINS_LOAD: coins %d PID %u", coins);

	peer->EncodeHeader(HEADER_DG_ITEMSHOP_COINS_LOAD, dwHandle, sizeof(DWORD));
	peer->EncodeDWORD(coins);
}
#endif