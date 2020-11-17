## search for:
class ThinBoard(Window):
	[...]

## add under:
class ThinBoardCircle(Window):

	CORNER_WIDTH = 4
	CORNER_HEIGHT = 4
	LINE_WIDTH = 4
	LINE_HEIGHT = 4
	BOARD_COLOR = 0xFF070707

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "d:/ymir work/ui/pattern/thinboardcircle/ThinBoard_Corner_"+dir+"_circle.tga" for dir in ["LeftTop","LeftBottom","RightTop","RightBottom"] ]
		LineFileNames = [ "d:/ymir work/ui/pattern/thinboardcircle/ThinBoard_Line_"+dir+"_circle.tga" for dir in ["Left","Right","Top","Bottom"] ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = Bar()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.SetColor(self.BOARD_COLOR)
		Base.Show()
		self.Base = Base

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class MouseReflector(Window):
	def __init__(self, parent):
		Window.__init__(self)
		self.SetParent(parent)
		self.AddFlag("not_pick")
		self.width = self.height = 0
		self.isDown = False
		self.isEmpty = False
		self.EmptyOverin = False

	def __del__(self):
		Window.__del__(self)

	def SetEmptyOverIn(self, overin):
		self.EmptyOverin = overin

	def SetEmpty(self, isempty):
		self.isEmpty = isempty

	def GetEmpty(self):
		return self.isEmpty

	def Down(self):
		self.isDown = True

	def Up(self):
		self.isDown = False

	def OnRender(self):

		if self.isDown:
			grp.SetColor(WHITE_COLOR)
		else:
			grp.SetColor(HALF_WHITE_COLOR)

		if self.isEmpty:
			if self.isDown:
				grp.SetColor(WHITE_COLOR)
			else:
				grp.SetColor(HALF_RED_COLOR)

			if self.EmptyOverin and not self.isDown:
				grp.SetColor(HALF_WHITE_COLOR)

		x, y = self.GetGlobalPosition()
		grp.RenderBar(x + 2, y + 2, self.GetWidth() - 4, self.GetHeight() - 4)

class CheckBox(ImageBox):
	def __init__(self, filename="d:/ymir work/ui/public/Parameter_Slot_01.sub"):
		ImageBox.__init__(self)

		self.LoadImage(filename)

		self.mouseReflector = MouseReflector(self)
		self.mouseReflector.SetSize(self.GetWidth(), self.GetHeight())

		image = MakeImageBox(self, "d:/ymir work/ui/public/check_image.sub", 0, 0)
		image.AddFlag("not_pick")
		image.SetWindowHorizontalAlignCenter()
		image.SetWindowVerticalAlignCenter()
		image.Hide()
		self.Enable = True
		self.image = image
		self.event = None
		self.uncheckEvent = None

		self.Show()

		self.mouseReflector.UpdateRect()

		self.SetCheck(False)

	def __del__(self):
		ImageBox.__del__(self)

	def IsChecked(self):
		if self.image.IsShow():
			return True
		else:
			return False

	def SetCheck(self, flag):
		if flag == True:
			self.image.Show()
		else:
			self.image.Hide()

	def Disable(self):
		self.Enable = False

	def SetEvent(self, event):
		self.event = event

	def SetUncheckEvent(self, event):
		self.uncheckEvent = event

	def OnMouseOverIn(self):
		if not self.Enable:
			return
		self.mouseReflector.Show()

	def OnMouseOverOut(self):
		if not self.Enable:
			return
		self.mouseReflector.Hide()

	def OnMouseLeftButtonDown(self):
		if not self.Enable:
			return
		self.mouseReflector.Down()

	def OnMouseLeftButtonUp(self):
		if not self.Enable:
			return
		self.mouseReflector.Up()
		if self.IsChecked():
			self.SetCheck(False)
			if self.uncheckEvent:
				self.uncheckEvent()
		else:
			self.SetCheck(True)
			if self.event:
				self.event()

## search for:
			elif Type == "bar":
				parent.Children[Index] = Bar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBar(parent.Children[Index], ElementValue, parent)

## add under:
			elif Type == "thinboardcircle" or Type == "thinboard_circle":
				parent.Children[Index] = ThinBoardCircle()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "check_box":
				parent.Children[Index] = CheckBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementWindow(parent.Children[Index], ElementValue, parent)