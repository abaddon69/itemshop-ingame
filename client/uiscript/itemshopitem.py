#!/usr/bin/python
#-*- coding: iso-8859-1 -*-
import uiScriptLocale

window = {
	"name" : "ItemShopItem",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 440,
	"height" : 60,

	"children" :
	(
		{
			"name" : "bar",
			"type" : "bar",

			"x" : 0,
			"y" : 0,

			"width" : 440,
			"height" : 60,

			"color" : 0x70000000,

			"children" :
			(
				{
					"name" : "slotbar",
					"type" : "image",

					"x" : 0,
					"y" : 0,

					"image" : "d:/ymir work/ui/tab_menu_01.tga",

					"children" : (
						{
							"name" : "name",
							"type" : "text",

							"x" : 8,
							"y" : 4,

							"text" : "",
						},
						{
							"name" : "price",
							"type" : "text",

							"x" : 368,
							"y" : 4,

							"outline" : "outline",

							"text" : "",
						},
					),
				},
				{
					"name" : "slot1",
					"type" : "slot",
					"x" : 16,
					"y" : 24,

					"width" : 32,
					"height" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",

					"slot" : (
						{"index":1, "x":0, "y":0, "width":32, "height":32},
					),
				},
				{
					"name" : "slot2",
					"type" : "slot",
					"x" : 16,
					"y" : 24,

					"width" : 32,
					"height" : 64,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",

					"slot" : (
						{"index":1, "x":0, "y":0, "width":32, "height":32},
						{"index":2, "x":0, "y":32, "width":32, "height":32},
					),
				},
				{
					"name" : "slot3",
					"type" : "slot",
					"x" : 16,
					"y" : 24,

					"width" : 32,
					"height" : 96,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",

					"slot" : (
						{"index":1, "x":0, "y":0, "width":32, "height":32},
						{"index":2, "x":0, "y":32, "width":32, "height":32},
						{"index":3, "x":0, "y":64, "width":32, "height":32},
					),
				},
				{
					"name" : "money_value",
					"type" : "text",

					"x" : 56,
					"y" : 20,

					"vertical_align" : "center",

					"text" : uiScriptLocale.ITEMSHOP_ITEM_INFO,
				},
				{
					"name": "buy_button",
					"type": "button",

					"x": 337,
					"y": 20,

					"vertical_align" : "center",

					"default_image": "d:/ymir work/ui/itemshop/buy_button_0.tga",
					"over_image": "d:/ymir work/ui/itemshop/buy_button_1.tga",
					"down_image": "d:/ymir work/ui/itemshop/buy_button_2.tga",

					"text": "",
				},
			),
		},
	),
}