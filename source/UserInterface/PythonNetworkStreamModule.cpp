// search for:
PyObject* netRegisterErrorLog(PyObject* poSelf, PyObject* poArgs)
{
	char * szLog;
	if (!PyTuple_GetString(poArgs, 0, &szLog))
		return Py_BuildException();

	return Py_BuildNone();
}

// add under:
#ifdef ENABLE_ITEMSHOP
PyObject* netSendItemShopOpenPacket(PyObject* poSelf, PyObject* poArgs)
{
	CPythonNetworkStream& rns = CPythonNetworkStream::Instance();
	rns.SendItemShopOpenPacket();

	return Py_BuildNone();
}

PyObject* netSendItemShopBuyPacket(PyObject* poSelf, PyObject* poArgs)
{

	int id, category, count;

	if (!PyTuple_GetInteger(poArgs, 0, &id))
		return Py_BuildException();

	if (!PyTuple_GetInteger(poArgs, 1, &category))
		return Py_BuildException();

	if (!PyTuple_GetInteger(poArgs, 2, &count))
		count = 1;

	CPythonNetworkStream& rns = CPythonNetworkStream::Instance();
	rns.SendItemShopBuyPacket(id, category, count);

	return Py_BuildNone();
}
#endif

// search for:
		{ "RegisterErrorLog",						netRegisterErrorLog,						METH_VARARGS },

// add under:
#ifdef ENABLE_ITEMSHOP
		{ "SendItemShopOpenPacket", netSendItemShopOpenPacket, METH_VARARGS },
		{ "SendItemShopBuyPacket", netSendItemShopBuyPacket, METH_VARARGS },
#endif