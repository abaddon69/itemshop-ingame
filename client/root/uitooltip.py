## search for:
import ui

## add under:
import itemshop

## search for:
	def SetItemToolTip(self, itemVnum, color=None):
		[...]

## add under:
	def SetItemShopToolTip(self, slotIndex, category):
		itemVnum = itemshop.GetItemID(slotIndex, category)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(itemshop.GetItemMetinSocket(slotIndex, category, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(itemshop.GetItemAttribute(slotIndex, category, i))

		self.AddItemData(itemVnum, metinSlot, attrSlot)