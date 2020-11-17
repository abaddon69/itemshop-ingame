## search for:
import event

## add under:
import uiItemShop

## search for:
		self.dlgRefineNew = uiRefine.RefineDialogNew()
		self.dlgRefineNew.Hide()

## add under:
		self.wndItemShop = uiItemShop.ItemShopWindow()
		self.wndItemShop.Hide()

## search for:
		if self.dlgExchange:
			self.dlgExchange.Destroy()

## add under:
		if self.wndItemShop:
			self.wndItemShop.Destroy()

## search for:
		del self.wndItemSelect

## add under:
		del self.wndItemShop