import ui, item, localeInfo, uiCommon, uiToolTip, net, constInfo, itemshop, player
from _weakref import proxy

countList = [1,2, 5, 10, 20, 50, 100, 200]
timeList = [localeInfo.SecondToDHMS(eval("itemshop.TIME_%02d" % i)) for i in xrange(itemshop.ITEMSHOP_TIME_MAX_NUM)]
priceList = [eval("itemshop.PRICE_%02d" % i) for i in xrange(itemshop.ITEMSHOP_TIME_MAX_NUM)]

class ItemShopWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.category = {}
		self.wndEditorWindow = None
		self.__isEditor = False
		self.editButton = None
		self.currentCategory = -1
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/itemshopwindow.py")

		except:
			import exception
			exception.Abort("ItemShopWindow.__LoadScript.LoadObject")

		try:
			self.listBox = NewListBox()
			self.listBox.SetParent(self.GetChild("items_board"))
			self.listBox.SetSize(440, 395)
			self.listBox.SetPosition(5, 9)
			self.listBox.Show()

			self.scrollBar = ui.ScrollBar()
			self.scrollBar.SetParent(self.GetChild("items_board"))
			self.scrollBar.SetPosition(30, 0)
			self.scrollBar.SetScrollBarSize(self.GetChild("items_board").GetHeight() - 16)
			self.scrollBar.SetWindowHorizontalAlignRight()
			self.scrollBar.SetWindowVerticalAlignCenter()
			self.scrollBar.Hide()

			self.listBox.SetScrollBar(self.scrollBar)

			self.listBoxCat = ui.UnfoldListBox2()
			self.listBoxCat.SetParent(self)
			self.listBoxCat.SetSize(180, 380)
			self.listBoxCat.SetPosition(16, 164-53)
			self.listBoxCat.SetYDif(3)
			self.listBoxCat.Show()

			self.listBoxCat.ClearItem()

			for i in xrange(13):
				self.category[i] = self.GetChild("category_button_%02d" % (i+1))
				self.category[i].SetText(eval("localeInfo.ITEMSHOP_CATEGORY_%02d" % (i+1)))
				self.category[i].SetEvent(lambda arg=i: self.__OnClickCategoryButton(arg))
				self.category[i].ButtonText.SetOutline()
				self.listBoxCat.InsertItem(self.category[i])
			self.moneyText = self.GetChild("money_value")
			##self.GetChild("Board").SetCloseEvent(self.OpenWindow)

		except:
			import exception
			exception.Abort("ItemShopWindow.__LoadScript.BindObject")

		self.SetCenterPosition()

	def Open(self):
		self.Show()
		self.__OnClickCategoryButton(0)

	def __OnClickCategoryButton(self, index):
		self.listBox.ClearItems()

		self.currentCategory = index

		for i in xrange(13):
			self.category[i].SetUp()

		self.category[index].Down()

		itemPos = itemshop.GetCategoryItemPos(index)

		for pos in itemPos:
			temp_item = ItemShopItem(pos, index)
			self.listBox.AppendItem(temp_item)

		self.scrollBar.Show()

		self.UpdateCoins()

	def SetEditorFlag(self, flag):
		self.__isEditor = flag

		if flag:

			self.editButton = ui.ExpandedButton()
			self.editButton.SetParent(self.GetChild("items_board"))
			self.editButton.SetUpVisual("d:/ymir work/ui/itemshop/edit_button.tga")
			self.editButton.SetOverVisual("d:/ymir work/ui/itemshop/edit_button.tga")
			self.editButton.SetDownVisual("d:/ymir work/ui/itemshop/edit_button.tga")
			self.editButton.SetWindowHorizontalAlignRight()
			self.editButton.SetWindowVerticalAlignBottom()
			self.editButton.SetPosition(30, 30)
			self.editButton.SetEvent(self.OpenEditorWindow)
			self.editButton.Show()

	def GetEditorFlag(self):
		return self.__isEditor
		
	def OpenEditorWindow(self):
		if not self.GetEditorFlag():
			return

		if not self.wndEditorWindow:
			self.wndEditorWindow = ItemShopEditorWindow()
			self.wndEditorWindow.Hide()

		self.wndEditorWindow.OpenWindow()

	def ClearItems(self):
		self.listBox.ClearItems()

	def Destroy(self):
		if self.wndEditorWindow:
			self.wndEditorWindow.Destroy()
			del self.wndEditorWindow

		self.Hide()
		self.ClearDictionary()

	def OnPressEscapeKey(self):
		self.Hide()
		return True

	def RequestOpen(self):
		if self.IsShow():
			self.Hide()
			return
		net.SendItemShopOpenPacket()

	def OpenWindow(self):
		if self.IsShow():
			self.Hide()
		else:
			self.Show()

	def UpdateCoins(self):
		self.moneyText.SetText(localeInfo.ITEMSHOP_YOUR_COINS % localeInfo.NumberToMoneyString(int(itemshop.GetCoins()))[:-5])

	def RefreshPage(self):
		scrollPos = self.listBox.GetScrollBarPosition()
		self.__OnClickCategoryButton(self.currentCategory)
		self.listBox.OnScroll(scrollPos)
		if self.wndEditorWindow:
			if self.wndEditorWindow.IsShow():
				self.wndEditorWindow.RefreshList()

import grp

class NewListBox(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		self.items = []
		self.selected = None
		self.basePos = 0
		self.itemWidth = 100
		self.itemStep = 4
		self.scrollbar = None
		self.scrollBarPos = 0.0

		self.selectEvent = None

	def SetSize(self, w, h):
		ui.Window.SetSize(self, w, h + self.itemStep)
		self.SetItemWidth(w)

		self.UpdateList()

	def SetScrollBar(self, scrollbar):
		self.scrollbar = scrollbar
		self.scrollbar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
		self.scrollbar.SetScrollStep(0.10)
		self.UpdateList()

	def CalcTotalItemHeight(self):
		total_height = 0
		for item in self.items:
			total_height += item.GetHeight()
			total_height += self.itemStep

		return total_height

	def ConfigureScrollBar(self):
		if self.scrollbar:
			itemheight = self.CalcTotalItemHeight()
			myheight = self.GetHeight() - 2 * self.itemStep
			dif = 0.97
			if itemheight > myheight and itemheight != 0:
				dif = 1.0 * myheight / itemheight

			self.scrollbar.SetMiddleBarSize(dif)

	def __OnScroll(self, position = None):
		pos = self.scrollbar.GetPos() if position == None else position
		self.scrollBarPos = pos
		toscr = self.CalcTotalItemHeight() - self.GetHeight() + 2 * self.itemStep
		self.basePos = toscr * pos

		self.UpdateList()

	def GetScrollBarPosition(self):
		return self.scrollBarPos

	def OnScroll(self, pos):
		self.__OnScroll(pos)

	def SelectItem(self, item):
		self.selected = item

		if self.selectEvent:
			self.selectEvent(item)

	def AppendItem(self, item):
		item.SetParent(self)
		item.SetWidth(self.itemWidth)
		item.Show()
		self.items.append(item)

		self.UpdateList()

	def RemoveItem(self, item):
		item.Hide()

		self.items.remove(item)
		self.UpdateList()

	def ClearItems(self):
		map(lambda wnd: wnd.Hide(), self.items)
		del self.items[:]

		self.basePos = 0
		if self.scrollbar:
			self.scrollbar.SetPos(0)
		self.UpdateList()

	def UpdateList(self):
		self.ConfigureScrollBar()
		self.RecalcItemPositions()

	def IsEmpty(self):
		return len(self.itemList) == 0

	def SetItemWidth(self, w):
		self.itemWidth = w
		for item in self.items:
			item.SetWidth(w)

	def RecalcItemPositions(self):
		curbp = self.basePos

		itemheight = self.CalcTotalItemHeight()
		myheight = self.GetHeight() - 2 * self.itemStep

		if itemheight < myheight:
			curbp = 0

		fromPos = curbp
		curPos = 0
		toPos = curbp + self.GetHeight()
		for item in self.items:
			hw = item.GetHeight()
			if curPos + hw < fromPos:
				item.Hide()
			elif curPos < fromPos and curPos + hw > fromPos:
				item.SetRenderMin(fromPos - curPos)
				item.Show()
			elif curPos < toPos and curPos + hw > toPos:
				item.SetRenderMax(toPos - curPos)
				item.Show()
			elif curPos > toPos:
				item.Hide()
			else:
				item.SetRenderMin(0)
				item.Show()

			item.SetPosition(0, curPos - fromPos)
			curPos += hw + self.itemStep

class NewListBoxItem(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		self.width = 0
		self.height = 0
		self.minh = 0
		self.maxh = 0

		self.components = []

	def __del__(self):
		ui.Window.__del__(self)

	def SetColor(self, color=0xff0099ff):
		self.color = color

	def SetParent(self, parent):
		ui.Window.SetParent(self, parent)

	def SetHeight(self, h):
		self.SetSize(self.width, h)

	def SetWidth(self, w):
		self.SetSize(w, self.height)

	def SetSize(self, w, h):
		self.width = w
		self.height = h
		self.maxh = h
		ui.Window.SetSize(self, w, h)

	def SetRenderMin(self, minh):
		self.minh = minh
		self.maxh = self.height
		self.RecalculateRenderedComponents()

	def SetRenderMax(self, maxh):
		self.maxh = maxh
		self.minh = 0
		self.RecalculateRenderedComponents()

	def RegisterComponent(self, component):
		mtype = type(component).__name__
		if mtype == "Bar":
			(x, y, w, h) = component.GetRect()
			(x, y) = component.GetLocalPosition()
			component.__list_data = [x, y, w, h]
		self.components.append(component)

	def UnregisterComponent(self, component):
		self.components.remove(component)
		#if component.__list_data:
		#	component.__list_data = None

	def RecalculateRenderedComponents(self):
		for component in self.components:
			(xl, yl) = component.GetLocalPosition()
			(x, y, w, h) = component.GetRect()
			mtype = type(component).__name__
			if mtype == "TextLine":
				(w, h) = component.GetTextSize()

			if yl + h < self.minh:
				component.Hide()
			elif yl > self.maxh:
				component.Hide()
			else:
				if mtype == "ExpandedImageBox" or mtype == "ExpandedButton":

					miny = 0
					if self.minh > 0 and yl < self.minh:
						miny = -float(self.minh - yl) / float(h)

					maxy = 0
					if h != 0:
						maxy = float(self.maxh - yl - h) / float(h)

					maxy = min(0, max(-1, maxy))

					component.SetRenderingRect(0.0, miny, 0.0, maxy)
					component.Show()

				else:
					if yl < self.minh or yl + h > self.maxh:
						component.Hide()
					else:
						component.Show()

	def OnRender(self):
		x, y = self.GetGlobalPosition()
		grp.SetColor(self.color)
		grp.RenderBar(x, y + self.minh, self.GetWidth(), self.maxh - self.minh)

import uiScriptLocale
class ItemShopItem(NewListBoxItem):
	def __init__(self, pos, category):
		NewListBoxItem.__init__(self)
		self.slot = []
		self.itemBuyQuestionDialog = None
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()
		self.__index = pos
		self.__category = category
		self.itemCount = 1
		self.__LoadWindow()

		self.SetColor(0x70000000)

	def __del__(self):
		NewListBoxItem.__del__(self)

	def Destroy(self):
		pass

	def __LoadWindow(self):

		self.slotBar = ui.ExpandedImageBox()
		self.slotBar.SetParent(self)
		self.slotBar.SetPosition(0, 0)
		self.slotBar.LoadImage("d:/ymir work/ui/tab_menu_01.tga")
		self.slotBar.Show()

		self.RegisterComponent(self.slotBar)

		self.nameText = ui.TextLine()
		self.nameText.SetParent(self.slotBar)
		self.nameText.SetPosition(8, 4)
		item.SelectItem(itemshop.GetItemID(self.__index, self.__category))
		self.nameText.SetText("%dx %s" % (itemshop.GetItemCount(self.__index, self.__category), item.GetItemName()))
		self.nameText.Show()

		self.RegisterComponent(self.nameText)

		self.priceText = ui.TextLine()
		self.priceText.SetParent(self.slotBar)
		self.priceText.SetPosition(368, 4)
		self.priceText.SetOutline(True)
		self.priceText.SetText(localeInfo.ITEMSHOP_ITEM_PRICE % localeInfo.NumberToMoneyString(itemshop.GetItemPrice(self.__index, self.__category))[:-5])
		self.priceText.Show()

		self.RegisterComponent(self.priceText)

		slotImageFileName = ["slot_32x32.tga", "slot_32x64.tga", "slot_32x96.tga"]
		for i in xrange(3):
			slot = ui.ExpandedImageBox()
			slot.SetParent(self)
			slot.SetPosition(16, 24)
			slot.LoadImage("d:/ymir work/ui/itemshop/%s" % (slotImageFileName[i]))
			slot.Show()
			slot.OnMouseOverIn = self.__OverInItem
			slot.OnMouseOverOut = self.__OverOutItem
			slot.Show()

			self.RegisterComponent(slot)

			self.slot.append(slot)

		self.itemImage = ui.ExpandedImageBox()
		self.itemImage.SetParent(self)
		self.itemImage.SetPosition(16, 24)
		self.itemImage.Show()

		self.itemImage.OnMouseOverIn = self.__OverInItem
		self.itemImage.OnMouseOverOut = self.__OverOutItem

		self.RegisterComponent(self.itemImage)

		self.itemInfoText = ui.TextLine()
		self.itemInfoText.SetParent(self.slotBar)
		self.itemInfoText.SetPosition(56, 20)
		self.itemInfoText.SetWindowVerticalAlignCenter()
		self.itemInfoText.SetText(uiScriptLocale.ITEMSHOP_ITEM_INFO)
		self.itemInfoText.Show()

		self.RegisterComponent(self.itemInfoText)

		self.buyButton = ui.ExpandedButton()
		self.buyButton.SetParent(self)
		self.buyButton.SetUpVisual("d:/ymir work/ui/itemshop/buy_button_0.tga")
		self.buyButton.SetOverVisual("d:/ymir work/ui/itemshop/buy_button_1.tga")
		self.buyButton.SetDownVisual("d:/ymir work/ui/itemshop/buy_button_2.tga")
		self.buyButton.SetPosition(337, 20)
		self.buyButton.SetEvent(ui.__mem_func__(self.__AskBuyItem))
		self.buyButton.Show()

		self.RegisterComponent(self.buyButton)

		self.__SetItem(itemshop.GetItemID(self.__index, self.__category))

	def __SetItem(self, vnum):
		for slot in self.slot:
			slot.Hide()
			try:
				self.UnregisterComponent(slot)
			except:
				pass

		item.SelectItem(vnum)
		width, height = item.GetItemSize()

		targetSlot = self.slot[height-1]
		targetSlot.Show()
		self.RegisterComponent(targetSlot)

		self.itemImage.LoadImage(item.GetIconImageFileName())
		self.SetSize(self.slotBar.GetWidth(), 60+32*(height-1))

		self.buyButton.SetPosition(self.buyButton.GetLeft(), self.GetHeight()-self.buyButton.GetHeight()-9)
		(w, h) = self.itemInfoText.GetTextSize()
		self.itemInfoText.SetPosition(self.itemInfoText.GetLeft(), self.GetHeight()-h-12-15)

	def __AskBuyItem(self):
		itemIndex = itemshop.GetItemID(self.__index, self.__category)
		itemPrice = itemshop.GetItemPrice(self.__index, self.__category)
		itemCount = itemshop.GetItemCount(self.__index, self.__category)

		item.SelectItem(itemIndex)
		itemName = item.GetItemName()

		itemBuyQuestionDialog = ItemQuestionDialog()
		#itemBuyQuestionDialog.SetText(localeInfo.ITEMSHOP_DO_YOU_BUY_ITEM(itemName, itemCount, localeInfo.NumberToMoneyString(itemPrice)[:-5]))
		itemBuyQuestionDialog.SetPrice(itemPrice)
		itemBuyQuestionDialog.SetCount(itemCount)
		itemBuyQuestionDialog.SetName(itemName)
		itemBuyQuestionDialog.SetAcceptEvent(lambda arg=True: self.__AnswerBuyItem(arg))
		itemBuyQuestionDialog.SetCancelEvent(lambda arg=False: self.__AnswerBuyItem(arg))
		itemBuyQuestionDialog.Open(itemIndex, itemshop.IsFixedCount(self.__index, self.__category))
		itemBuyQuestionDialog.index = self.__index
		itemBuyQuestionDialog.category = self.__category
		itemBuyQuestionDialog.UpdateText()
		self.itemBuyQuestionDialog = itemBuyQuestionDialog

	def __AnswerBuyItem(self, flag):

		if flag:
			import dbg
			dbg.TraceError(str(self.itemBuyQuestionDialog.GetItemCount()))
			net.SendItemShopBuyPacket(self.__index, self.__category, self.itemBuyQuestionDialog.GetItemCount() if self.itemBuyQuestionDialog else 1)

		self.itemBuyQuestionDialog.Close()
		self.itemBuyQuestionDialog = None

	def __OverInItem(self):
		if self.tooltipItem:
			self.tooltipItem.SetItemShopToolTip(self.__index, self.__category)

	def __OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

class ItemQuestionDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.comboBox = None
		self.__CreateDialog()

		self.tooltipItem = uiToolTip.ItemToolTip()
		self.toolTip = uiToolTip.ToolTip()

		self.count = 0
		self.name = ""
		self.price = ""
		self.list = []
		self.index = -1
		self.isCostume = False
		self.category = -1

		self.itemCount = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

		self.titleBar = ui.TitleBar()
		self.titleBar.SetParent(self.board)
		self.titleBar.MakeTitleBar(244, "yellow")
		self.titleBar.SetPosition(8, 7)
		self.titleBar.Show()

		self.titleName = ui.TextLine()
		self.titleName.SetParent(self.titleBar)
		self.titleName.SetPosition(0, 4)
		self.titleName.SetWindowHorizontalAlignCenter()
		self.titleName.SetHorizontalAlignCenter()
		self.titleName.Show()

		self.PrepareComboBox()

		self.slotList = []
		for i in xrange(3):
			slot = ui.ImageBox()
			slot.LoadImage("d:/ymir work/ui/public/slot_base.sub")
			slot.SetParent(self)
			self.slotList.append(slot)

	def GetItemCount(self):
		if self.isCostume:
			try:
				return timeList.index(self.itemCount)
			except ValueError:
				return 0
		else:
			return self.itemCount

	def SetItemCount(self, count):
		self.itemCount = self.list[count]
		if self.isCostume:
			self.comboBox.SetCurrentItem(timeList[self.GetItemCount()])
		else:
			self.comboBox.SetCurrentItem(str(self.list[count]))
		self.SetTop()
		self.UpdateText()

	def SetCount(self, count):
		self.itemCount = count

	def UpdateText(self):
		if self.isCostume:
			self.textLine.SetText(localeInfo.ITEMSHOP_DO_YOU_BUY_ITEM(self.name, 1, localeInfo.NumberToMoneyString(self.price + priceList[self.GetItemCount()])[:-5]))
		else:
			self.textLine.SetText(localeInfo.ITEMSHOP_DO_YOU_BUY_ITEM(self.name, self.itemCount, localeInfo.NumberToMoneyString(self.price*self.itemCount)[:-5]))

	def SetName(self, name):
		self.name = name

	def SetPrice(self, price):
		self.price = price

	def PrepareComboBox(self, isCostume=False):
		self.isCostume = isCostume
		if self.comboBox:
			self.comboBox.Hide()
			del self.comboBox

		self.comboBox = ui.ComboBox()
		self.comboBox.SetParent(self)
		self.comboBox.SetPosition(64, 62)

		self.list = countList if not isCostume else timeList
		self.comboBox.SetSize(50 if not isCostume else 200, 20)
		self.comboBox.SetEvent(
			lambda itemCount, argSelf=proxy(self): argSelf.SetItemCount(itemCount))
		for i in xrange(len(self.list)):
			self.comboBox.InsertItem(i, str(self.list[i]))
		self.comboBox.SetCurrentItem(str(self.list[0]))

		self.comboBox.Hide()

	def Open(self, vnum, fixed_count):
		item.SelectItem(vnum)
		xSlotCount, ySlotCount = item.GetItemSize()

		xSlotPos = 114 if fixed_count else 16

		newHeight = 0

		self.PrepareComboBox(item.GetItemType() == item.ITEM_TYPE_COSTUME and not fixed_count)
		if not fixed_count:
			self.comboBox.Show()
		else:
			self.comboBox.Hide()

		slotGrid = ui.SlotWindow()
		slotGrid.SetParent(self)
		slotGrid.SetPosition(xSlotPos, 62)
		slotGrid.AppendSlot(0, 0, 0, 32 * xSlotCount, 32 * ySlotCount)
		slotGrid.AddFlag("not_pick")
		slotGrid.Show()
		self.slotGrid = slotGrid

		if self.count > 1 and vnum != 1:
			self.slotGrid.SetItemSlot(0, vnum, self.count)
		else:
			self.slotGrid.SetItemSlot(0, vnum)

		self.SetSize(260, 300)
		self.board.SetSize(260, 110 + 32 * ySlotCount + newHeight)
		self.textLine.SetPosition(0, 44)

		for i in xrange(min(3, ySlotCount)):
			self.slotList[i].SetPosition(xSlotPos, 30 + ySlotCount * 32 - i * 32)
			if vnum != 1:
				self.slotList[i].OnMouseOverIn = lambda arg="": self.OverInItem(arg)
				self.slotList[i].OnMouseOverOut = lambda arg=self.tooltipItem: self.OverOutItem(arg)
			else:
				self.slotList[i].OnMouseOverIn = lambda arg=localeInfo.MONETARY_UNIT0: self.OverInToolTip(arg)
				self.slotList[i].OnMouseOverOut = lambda: self.OverOutToolTip()
			self.slotList[i].Show()

		self.GetChild("accept").SetPosition(-40, 74 + 32 * ySlotCount + newHeight)
		self.GetChild("cancel").SetPosition(40, 74 + 32 * ySlotCount + newHeight)

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.titleName.SetText(item.GetItemName())

		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def SetCloseEvent(self, event):
		self.titleBar.SetCloseEvent(event)

	def SetMessage(self, text):
		self.textLine.SetText(text)

	def OverInToolTip(self, arg):
		self.toolTip.ClearToolTip()
		self.toolTip.AppendTextLine(arg, 0xffffff00)
		self.toolTip.Show()

	def OverOutToolTip(self):
		self.toolTip.Hide()

	def OverInItem(self, slot):
		self.tooltipItem.SetItemShopToolTip(self.index, self.category)

	def OverOutItem(self, tooltipItem):
		if None != tooltipItem:
			self.tooltipItem.HideToolTip()
			self.tooltipItem.ClearToolTip()

	def Close(self):
		self.ClearDictionary()
		self.slotList = []
		self.titleBar = None
		self.titleName = None
		self.itemPrice = None
		self.slotGrid = None

		self.toolTip = None
		self.tooltipItem = None
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()

		return True

WEAPON_SOCKETS = item.GetWeaponSockets()
BODY_SOCKETS = item.GetBodySockets()
ITEM_LIST = item.GetNames()

class ItemShopEditorWindow(ui.ScriptWindow):
	class Item(ui.Bar):
		def __init__(self):
			ui.Bar.__init__(self)
			self.__onClickEvent = None
			self.__textLine = None
			self.__CreateWindow()

		def __del__(self):
			ui.Bar.__del__(self)

		def __CreateWindow(self):
			self.__textLine = ui.TextLine()
			self.__textLine.SetParent(self)
			self.__textLine.SetPosition(32, 0)

			self.__textLine.Show()

			self.OnMouseLeftButtonDown = self.__OnClickButton
			self.__textLine.OnMouseLeftButtonDown = self.__OnClickButton

			self.OnMouseOverIn = self.__OnOverIn
			self.__textLine.OnMouseOverIn = self.__OnOverIn

			self.OnMouseOverOut = self.__OnOverOut
			self.__textLine.OnMouseOverOut = self.__OnOverOut

			self.SetSize(self.GetWidth(), self.GetHeight())
			self.SetColor(0x00000000)

		def __OnClickButton(self):
			if self.__onClickEvent:
				self.__onClickEvent()

			self.SetColor(grp.GenerateColor(0.0, 0.0, 0.5, 0.4))

		def SetText(self, text):
			self.__textLine.SetText(localeInfo.ITEMSHOP_EDITOR_ITEM_PREFIX % text)

		def SetEvent(self, event):
			self.__onClickEvent = event

		def GetWidth(self):
			return 206

		def GetHeight(self):
			return 20

		def __OnOverIn(self):
			self.SetColor(ui.SELECT_COLOR)

		def __OnOverOut(self):
			self.SetColor(0x00000000)

	class Expander(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.__expandEvent = None
			self.__foldEvent = None
			self.__normalButton = None
			self.__expandedButton = None
			self.__isExpanded = False
			self.__CreateWindow()

		def __del__(self):
			ui.Window.__del__(self)

		def __CreateWindow(self):
			self.__normalButton = ui.Button()
			self.__normalButton.SetParent(self)
			self.__normalButton.SetUpVisual("d:/ymir work/ui/game/sphaera/list_expander_closed_normal.tga")
			self.__normalButton.SetOverVisual("d:/ymir work/ui/game/sphaera/list_expander_closed_hover.tga")
			self.__normalButton.SetDownVisual("d:/ymir work/ui/game/sphaera/list_expander_closed_hover.tga")
			self.__normalButton.SetEvent(self.__OnClickButton)
			self.__normalButton.Show()

			self.__expandedButton = ui.Button()
			self.__expandedButton.SetParent(self)
			self.__expandedButton.SetUpVisual("d:/ymir work/ui/game/sphaera/list_expander_open_normal.tga")
			self.__expandedButton.SetOverVisual("d:/ymir work/ui/game/sphaera/list_expander_open_hover.tga")
			self.__expandedButton.SetDownVisual("d:/ymir work/ui/game/sphaera/list_expander_open_hover.tga")
			self.__expandedButton.SetEvent(self.__OnClickButton)
			self.__expandedButton.Hide()

			self.__UpdateSize()

		def __OnClickButton(self):
			if self.__isExpanded:
				self.__expandedButton.Hide()
				self.__normalButton.Show()

				self.__isExpanded = not self.__isExpanded

				if self.__foldEvent:
					self.__foldEvent()
			else:
				self.__expandedButton.Show()
				self.__normalButton.Hide()

				self.__isExpanded = not self.__isExpanded

				if self.__expandEvent:
					self.__expandEvent()

			self.__UpdateSize()

		def __UpdateSize(self):
			width = self.GetWidth()
			height = self.GetHeight()

			self.SetSize(width, height)

		def SetText(self, text):
			self.__normalButton.SetText(text)
			self.__expandedButton.SetText(text)

		def SetExpandEvent(self, event):
			self.__expandEvent = event

		def SetFoldEvent(self, event):
			self.__foldEvent = event

		def IsExpanded(self):
			return self.__isExpanded

		def GetWidth(self):
			return self.__expandedButton.GetWidth() if self.__isExpanded else self.__normalButton.GetWidth()

		def GetHeight(self):
			return self.__expandedButton.GetHeight() if self.__isExpanded else self.__normalButton.GetHeight()

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__obj = {"expander": {}, "items": {}, "socket" : {}, "socket_text" : {}, "attr" : {}, "attr_text" : {}, "attr_value" : {}, "attr_value_text" : {}}
		self.__itemIndex = self.__itemCategory = -1
		self.itemToolTip = uiToolTip.ItemToolTip()
		self.itemToolTip.Hide()
		self.__LoadScript()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/itemshopeditorwindow.py")
		except:
			import exception
			exception.Abort("ItemShopEditorWindow.__LoadScript.LoadObject")

		self.GetChild("Board").SetCloseEvent(self.OpenWindow)
		self.itemNameValue = self.GetChild("item_name_value")
		self.itemNameSlot = self.GetChild("item_name_slot")
		self.itemCountValue = self.GetChild("item_count_value")
		self.itemPriceValue = self.GetChild("item_price_value")
		self.itemSlot = self.GetChild("item_slot")
		self.unfixedCountCheckBox = self.GetChild("unfixed_price_checkbox")

		self.GetChild("item_count_slot").OnMouseLeftButtonDown = self.itemCountValue.SetFocus
		self.GetChild("item_price_slot").OnMouseLeftButtonDown = self.itemPriceValue.SetFocus

		self.itemNameSlot.OnMouseLeftButtonDown = self.__OnClickItemNameSlot
		self.itemNameValue.OnMouseLeftButtonDown = self.__OnClickItemNameSlot

		self.itemSlot.SetOverInItemEvent(self.__OverInItem)
		self.itemSlot.SetOverOutItemEvent(self.__OverOutItem)

		self.editButton = self.GetChild("edit_button")
		self.editButton.SetEvent(self.__OnClickEditButton)

		self.addButton = self.GetChild("add_button")
		self.addButton.SetEvent(self.__OnClickAddButton)

		self.deleteButton = self.GetChild("delete_button")
		self.deleteButton.SetEvent(self.__OnClickDeleteButton)

		self.unfoldListBox = self.GetChild("categories_listbox")

		for i in xrange(13):
			self.__obj["items"][i] = {}

			self.__obj["expander"][i] = self.Expander()
			self.__obj["expander"][i].SetText(eval("localeInfo.ITEMSHOP_CATEGORY_%02d" % (i + 1)))
			self.__obj["expander"][i].Show()
			self.__obj["expander"][i].SetExpandEvent(lambda : self.RefreshList())
			self.__obj["expander"][i].SetFoldEvent(lambda : self.RefreshList())

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			self.__obj["socket"][i] = self.GetChild("socket_window_%02d" % (i+1))
			self.__obj["socket_text"][i] = self.GetChild("socket_text_%02d" % (i+1))

			self.__obj["socket"][i].OnMouseLeftButtonDown = lambda arg=i: self.__OnClickSocketWindow(arg)
			self.__obj["socket_text"][i].OnMouseLeftButtonDown = lambda arg=i: self.__OnClickSocketWindow(arg)

		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			self.__obj["attr"][i] = self.GetChild("attr_window_%02d" % (i+1))
			self.__obj["attr_text"][i] = self.GetChild("attr_text_%02d" % (i+1))

			self.__obj["attr_value"][i] = self.GetChild("attr_value_window_%02d" % (i+1))
			self.__obj["attr_value_text"][i] = self.GetChild("attr_value_text_%02d" % (i+1))

			self.__obj["attr"][i].OnMouseLeftButtonDown = lambda arg=i: self.__OnClickAttrWindow(arg)
			self.__obj["attr_text"][i].OnMouseLeftButtonDown = lambda arg=i: self.__OnClickAttrWindow(arg)

			self.__obj["attr_value"][i].OnMouseLeftButtonDown = lambda arg=i: self.__OnClickAttrValueWindow(arg)
			self.__obj["attr_value_text"][i].OnMouseLeftButtonDown = lambda arg=i: self.__OnClickAttrValueWindow(arg)

		self.__SetSlotData()

		self.RefreshList()
		self.wndSelector = ItemShopSelectListWindow()
		self.wndSelector.Hide()

	def RefreshList(self):
		self.unfoldListBox.ClearItem()
		for key, obj in self.__obj["expander"].iteritems():
			self.unfoldListBox.InsertItem(obj)
			if obj.IsExpanded():

				itemPos = itemshop.GetCategoryItemPos(key)

				for itemData in itemPos:
					itemVnum = itemshop.GetItemID(itemData, key)
					item.SelectItem(itemVnum)

					temp_item = self.Item()
					temp_item.SetText(item.GetItemName())
					temp_item.SetEvent(lambda index=itemData, cat=key: self.__OnSelectItem(index, cat))
					self.unfoldListBox.InsertItem(temp_item)

				temp_item = self.Item()
				temp_item.SetText(localeInfo.ITEMSHOP_EDITOR_ADD_ITEM)
				temp_item.SetEvent(lambda index=-1, cat=key: self.__OnSelectItem(index, cat))
				self.unfoldListBox.InsertItem(temp_item)
		self.__OnSelectItem(-1, -1)

	def __OnSelectItem(self, index, cat):

		self.__itemIndex = index
		self.__itemCategory = cat

		if index == -1:

			self.itemNameValue.SetText(localeInfo.ITEMSHOP_SELECT_ITEM)
			self.itemCountValue.SetText("1")
			self.itemPriceValue.SetText("1")

			self.itemSlot.ClearSlot(0)

			self.__SetSlotData()

			self.deleteButton.Hide()
			self.editButton.Hide()
			if cat == -1:
				self.addButton.Hide()
			else:
				self.addButton.Show()

		else:

			itemVnum = itemshop.GetItemID(index, cat)

			if not itemVnum:
				return

			item.SelectItem(itemVnum)
			self.itemNameValue.SetText(item.GetItemName())
			self.itemNameValue.itemVnum = itemVnum
			self.itemCountValue.SetText(str(itemshop.GetItemCount(index, cat)))
			self.itemPriceValue.SetText(str(itemshop.GetItemPrice(index, cat)))

			self.itemSlot.SetItemSlot(0, itemVnum, 0)

			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(itemshop.GetItemMetinSocket(index, cat, i))
			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(itemshop.GetItemAttribute(index, cat, i))

			self.__SetSlotData(metinSlot, attrSlot)

			self.deleteButton.Show()
			self.editButton.Show()
			self.addButton.Hide()

	def __OnClickAttrWindow(self, slot):
		if self.__itemCategory == -1:
			return

		list = uiToolTip.ItemToolTip.AFFECT_DICT

		self.wndSelector.PrepareList("attr", list)
		self.wndSelector.Show()
		self.wndSelector.SetTop()
		self.wndSelector.SetSelectedSlot(self.__obj["attr_text"][slot])
		self.wndSelector.SetValueSlot(self.__obj["attr_value_text"][slot])

	def __OnClickSocketWindow(self, slot):
		if self.__itemCategory == -1:
			return

		itemVnum = itemshop.GetItemID(self.__itemIndex, self.__itemCategory)

		if not itemVnum:
			return

		item.SelectItem(itemVnum)

		list = {}

		if item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() != item.WEAPON_ARROW:
			list = WEAPON_SOCKETS

		elif item.GetItemType() == item.ITEM_TYPE_ARMOR and item.GetItemSubType() == item.ARMOR_BODY:
			list = BODY_SOCKETS

		else:
			list = {}

		self.wndSelector.PrepareList("socket", list)
		self.wndSelector.Show()
		self.wndSelector.SetTop()
		self.wndSelector.SetSelectedSlot(self.__obj["socket_text"][slot])

	def __OnClickAttrValueWindow(self, slot):
		if self.__itemCategory == -1:
			return

		editLine = self.__obj["attr_value_text"][slot]
		editLine.SetFocus()

	def __OnClickEditButton(self):

		itemIndex = self.__itemIndex
		itemCategory = self.__itemCategory

		itemVnum = itemshop.GetItemID(itemIndex, itemCategory)
		itemPrice = int(self.itemPriceValue.GetText())
		itemCount = int(self.itemCountValue.GetText())

		itemFixedCountFlag = bool(self.unfixedCountCheckBox.IsChecked())

		itemSocket = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			itemSocket.append(int(self.__obj["socket_text"][i].itemVnum))

		itemAttr = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			itemAttr.append([int(self.__obj["attr_text"][i].attrValue), int(self.__obj["attr_value_text"][i].GetText())])

		itemshop.SendItemShopPacket(itemIndex, itemCategory, itemVnum, itemPrice, itemCount, itemFixedCountFlag, itemSocket, itemAttr, itemshop.EDITOR_FLAG_EDIT)

	def __OnClickAddButton(self):
		itemIndex = 0
		itemCategory = self.__itemCategory

		itemVnum = self.itemNameValue.itemVnum
		itemPrice = int(self.itemPriceValue.GetText())
		itemCount = int(self.itemCountValue.GetText())

		itemFixedCountFlag = bool(self.unfixedCountCheckBox.IsChecked())

		itemSocket = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			itemSocket.append(int(self.__obj["socket_text"][i].itemVnum))

		itemAttr = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			itemAttr.append([int(self.__obj["attr_text"][i].attrValue), int(self.__obj["attr_value_text"][i].GetText())])

		itemshop.SendItemShopPacket(itemIndex, itemCategory, itemVnum, itemPrice, itemCount, itemFixedCountFlag, itemSocket, itemAttr, itemshop.EDITOR_FLAG_ADD)

		self.__OnSelectItem(-1, -1)

	def __OnClickDeleteButton(self):
		itemIndex = self.__itemIndex
		itemCategory = self.__itemCategory

		itemshop.SendItemShopPacket(itemIndex, itemCategory, 0, 0, 0, 0, [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)], [(0, 0) for j in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)], itemshop.EDITOR_FLAG_DELETE)

		self.__itemIndex = -1
		self.__itemCategory = -1

	def __OnClickItemNameSlot(self):
		if self.__itemIndex == -1 and self.__itemCategory != -1:

			list = ITEM_LIST

			self.wndSelector.PrepareList("item", list)
			self.wndSelector.Show()
			self.wndSelector.SetTop()
			self.itemNameValue.itemVnum = 0
			self.wndSelector.SetSelectedSlot(self.itemNameValue)
			self.wndSelector.SetItemSlot(self.itemSlot)

	def __SetSlotData(self, sockets = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)], attrs = [(0, 0) for j in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]):
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			name = localeInfo.ITEMSHOP_SELECT_SOCKET
			if sockets[i]:
				item.SelectItem(sockets[i])
				name = item.GetItemName()

			self.__obj["socket_text"][i].SetText(name)
			self.__obj["socket_text"][i].itemVnum = sockets[i]

		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			name = localeInfo.ITEMSHOP_SELECT_BONUS
			if attrs[i][0]:
				name = GetAffectString(attrs[i][0])

			self.__obj["attr_text"][i].SetText(name)
			self.__obj["attr_text"][i].attrValue = attrs[i][0]
			self.__obj["attr_value_text"][i].SetText(str(attrs[i][1]))

	def __OverInItem(self, slotPos):
		if self.itemToolTip:
			itemVnum = getattr(self.itemNameValue, "itemVnum", None)
			if itemVnum:

				itemSocket = []
				for i in xrange(player.METIN_SOCKET_MAX_NUM):
					itemSocket.append(int(self.__obj["socket_text"][i].itemVnum))

				itemAttr = []
				for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
					itemAttr.append([int(self.__obj["attr_text"][i].attrValue), int(self.__obj["attr_value_text"][i].GetText())])

				self.itemToolTip.ClearToolTip()
				self.itemToolTip.AddRefineItemData(itemVnum, itemSocket, itemAttr)
				self.itemToolTip.ShowToolTip()


	def __OverOutItem(self):
		if self.itemToolTip:
			self.itemToolTip.HideToolTip()

	def OpenWindow(self):
		if self.IsShow():
			self.Hide()
		else:
			self.Show()
			self.SetCenterPosition()
			self.SetTop()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

	def OnPressEscapeKey(self):
		self.Hide()
		return True

def GetAffectString(affectIndex):
	affectName = uiToolTip.ItemToolTip().GetAffectString(affectIndex, 99)
	affectName = affectName.replace("+99", "")
	affectName = affectName.replace("+99%", "")
	affectName = affectName.replace("99%", "")
	affectName = affectName.replace("99", "")
	affectName = affectName.replace("%", "")
	affectName = affectName.replace(":", "")
	return affectName

class ItemShopSelectListWindow(ui.ScriptWindow):
	class ItemShopSelectListItem(ui.ListBoxEx.Item):
		def __init__(self, text, index):
			ui.ListBoxEx.Item.__init__(self)
			self.__textLine = self.__CreateTextLine(text)
			self.__index = index

		def __del__(self):
			ui.ListBoxEx.Item.__del__(self)

		def SetSize(self, width, height):
			ui.ListBoxEx.Item.SetSize(self, 300, height)

		def __CreateTextLine(self, text):
			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(0, 1)
			textLine.SetText(text)
			textLine.UpdateRect()
			textLine.Show()
			return textLine

		def GetItemIndex(self):
			return self.__index

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__selectedSlot = None
		self.__selectedValueSlot = None
		self.__selectedItemSlot = None
		self.__type = ""
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pythonScriptLoader = ui.PythonScriptLoader()
			pythonScriptLoader.LoadScriptFile(self, "uiscript/itemshopselectlist.py")
		except:
			import exception
			exception.Abort("ItemShopSelectListWindow.__LoadScript.LoadObject")

		try:
			self.listBox = self.GetChild("list_box_ex")
			self.scrollBar = self.GetChild("scroll_bar")
			self.board = self.GetChild("board")
			self.itemNameSlot = self.GetChild("item_name_slot")
			self.itemNameValue = self.GetChild("item_name_value")
			self.itemNameValue.OnIMEUpdate = self.__OnItemNameValueIMEUpdate
		except:

			import exception
			exception.Abort("ItemShopSelectListWindow.__LoadScript.BindObject")

		self.listBox.SetScrollBar(self.scrollBar)
		self.listBox.SetSelectEvent(self.__OnSelectItem)

		self.itemNameSlot.OnMouseLeftButtonDown = self.__OnClickItemNameSlot

		self.board.SetCloseEvent(self.Hide)

	def PrepareList(self, type, objects, skipText=False):

		self.listBox.RemoveAllItems()

		self.listBox.AppendItem(self.ItemShopSelectListItem(localeInfo.ITEMSHOP_SELECT_EMPTY, 0))

		if type == "socket":

			self.listBox.SetViewItemCount(18)
			self.itemNameSlot.Hide()
			self.itemNameValue.Hide()

			for obj in objects:
				item.SelectItem(obj)
				self.listBox.AppendItem(self.ItemShopSelectListItem(item.GetItemName(), obj))
			self.board.SetTitleName(localeInfo.ITEMSHOP_SELECT_SOCKET)

		elif type == "attr":

			self.listBox.SetViewItemCount(18)
			self.itemNameSlot.Hide()
			self.itemNameValue.Hide()

			for obj in objects.keys():
				self.listBox.AppendItem(self.ItemShopSelectListItem(GetAffectString(obj), obj))

			self.board.SetTitleName(localeInfo.ITEMSHOP_SELECT_BONUS)

		if type == "item":

			self.listBox.SetViewItemCount(17)
			self.itemNameSlot.Show()
			self.itemNameValue.Show()
			self.itemNameValue.SetFocus()

			for obj in objects:
				if obj["name"]:
					self.listBox.AppendItem(self.ItemShopSelectListItem(obj["name"], obj["vnum"]))
			self.board.SetTitleName(localeInfo.ITEMSHOP_SELECT_ITEM)
			if not skipText:
				self.itemNameValue.SetText(localeInfo.ITEMSHOP_SELECT_ITEM)

		self.__type = type

	def __OnSelectItem(self, obj):
		if self.__selectedSlot:
			if self.__type == "socket":
				itemVnum = obj.GetItemIndex()
				if itemVnum == 0:
					self.__selectedSlot.SetText(localeInfo.ITEMSHOP_SELECT_EMPTY)
				else:
					item.SelectItem(itemVnum)
					self.__selectedSlot.SetText(item.GetItemName())
				self.__selectedSlot.itemVnum = itemVnum
			elif self.__type == "attr":
				attrValue = obj.GetItemIndex()
				if attrValue == 0:
					self.__selectedSlot.SetText(localeInfo.ITEMSHOP_SELECT_EMPTY)
				else:
					self.__selectedSlot.SetText(GetAffectString(attrValue))

				self.__selectedSlot.attrValue = attrValue
				self.__selectedValueSlot.SetFocus()

			elif self.__type == "item":
				itemVnum = obj.GetItemIndex()
				if itemVnum == 0:
					self.__selectedSlot.SetText(localeInfo.ITEMSHOP_SELECT_EMPTY)
				else:
					item.SelectItem(itemVnum)
					self.__selectedSlot.SetText(item.GetItemName())
				if self.__selectedItemSlot:
					self.__selectedItemSlot.SetItemSlot(0, itemVnum, 0)
				self.__selectedSlot.itemVnum = itemVnum

		self.Hide()

	def SetSelectedSlot(self, slot):
		self.__selectedSlot = slot

		self.__selectedValueSlot = None
		self.__selectedItemSlot = None

	def SetValueSlot(self, slot):
		self.__selectedValueSlot = slot

	def SetItemSlot(self, slot):
		self.__selectedItemSlot = slot

	def __OnItemNameValueIMEUpdate(self):
		ui.EditLine.OnIMEUpdate(self.itemNameValue)
		self.__Search(self.itemNameValue.GetText())

	def __Search(self, destName = ""):
		self.listBox.RemoveAllItems()

		list = []

		if destName:
			for item in ITEM_LIST:
				name = item["name"]

				if len(name):
					if name.lower().find(destName.lower()) != -1:
						list.append(item)
		else:
			list = ITEM_LIST

		self.PrepareList("item", list, True)

	def __OnClickItemNameSlot(self):
		from difflib import SequenceMatcher
		text = self.itemNameValue.GetText().lower()
		destText = localeInfo.ITEMSHOP_SELECT_ITEM.lower()
		if SequenceMatcher(None, text, destText).ratio() >= 0.75:
			self.itemNameValue.SetText("")
