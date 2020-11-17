## search for:
	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

## replace it with:
	def RefreshItemSlot(self):
		try:
			self.interface.wndItemShop.UpdateCoins()
		except:
			pass
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

## i don't know how do you want it to be open, but this is a function that does it
	def __OnClickItemShopButton(self):
		self.interface.wndItemShop.RequestOpen()