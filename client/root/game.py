## search for:
	def OnShopError(self, type):
		[...]

## add under:
	def OnItemShopError(self, type):
		try:
			self.PopupMessage(localeInfo.ITEMSHOP_ERROR_DICT[type])
		except KeyError:
			self.PopupMessage(localeInfo.SHOP_ERROR_UNKNOWN % (type))

## search for:
	def __PlayMusic(self, flag, filename):
		[...]

## add under:
	def BINARY_ItemShopOpen(self):
		self.interface.wndItemShop.Open()

	def BINARY_ItemShopSetEditorFlag(self, flag):
		self.interface.wndItemShop.SetEditorFlag(flag)

	def BINARY_ItemShopRefresh(self):
		self.interface.wndItemShop.RefreshPage()