#!/usr/bin/python
#-*- coding: iso-8859-1 -*-
import uiScriptLocale

window = {
	"name" : "ItemShopDialog",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 707,
	"height" : 503,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "image",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width": 707,
			"height": 503,

			"image" : "d:/ymir work/ui/itemshop/bg.tga",

			##"title" : uiScriptLocale.ITEMSHOP_TITLE,

			"children" :
			(
				{
					"name": "logo",
					"type": "image",

					"x": 22,
					"y" : 24,

					"image" : "d:/ymir work/ui/itemshop/logo.tga",
				},
				{
					"name": "categories_board",
					"type": "window",

					"x": 12,
					"y" : 102,

					"width" : 170,
					"height" : 413,

					"children" : (
						{
							"name": "category_button_01",
							"type": "radio_button",

							"x": 11,
							"y": 9,

							"default_image": "d:/ymir work/ui/itemshop/category_button_01.tga",
							"over_image": "d:/ymir work/ui/itemshop/category_button_02.tga",
							"down_image": "d:/ymir work/ui/itemshop/category_button_03.tga",

							"text": "",
						},
						{
							"name": "category_button_02",
							"type": "radio_button",

							"x": 11,
							"y": 9 + 34 * 1,

							"default_image": "d:/ymir work/ui/itemshop/category_button_01.tga",
							"over_image": "d:/ymir work/ui/itemshop/category_button_02.tga",
							"down_image": "d:/ymir work/ui/itemshop/category_button_03.tga",

							"text": "",
						},
						{
							"name": "category_button_03",
							"type": "radio_button",

							"x": 11,
							"y": 9 + 34 * 2,

							"default_image": "d:/ymir work/ui/itemshop/category_button_01.tga",
							"over_image": "d:/ymir work/ui/itemshop/category_button_02.tga",
							"down_image": "d:/ymir work/ui/itemshop/category_button_03.tga",

							"text": "",
						},
						{
							"name": "category_button_04",
							"type": "radio_button",

							"x": 11,
							"y": 9 + 34 * 3,

							"default_image": "d:/ymir work/ui/itemshop/category_button_01.tga",
							"over_image": "d:/ymir work/ui/itemshop/category_button_02.tga",
							"down_image": "d:/ymir work/ui/itemshop/category_button_03.tga",

							"text": "",
						},
						{
							"name": "category_button_05",
							"type": "radio_button",

							"x": 11,
							"y": 9 + 34 * 4,

							"default_image": "d:/ymir work/ui/itemshop/category_button_01.tga",
							"over_image": "d:/ymir work/ui/itemshop/category_button_02.tga",
							"down_image": "d:/ymir work/ui/itemshop/category_button_03.tga",

							"text": "",
						},
						{
							"name": "category_button_06",
							"type": "radio_button",

							"x": 11,
							"y": 9 + 34 * 5,

							"default_image": "d:/ymir work/ui/itemshop/category_button_01.tga",
							"over_image": "d:/ymir work/ui/itemshop/category_button_02.tga",
							"down_image": "d:/ymir work/ui/itemshop/category_button_03.tga",
							"text": "",
						},
						{
							"name": "category_button_07",
							"type": "radio_button",

							"x": 11,
							"y": 9 + 34 * 6,

							"default_image": "d:/ymir work/ui/itemshop/category_button_01.tga",
							"over_image": "d:/ymir work/ui/itemshop/category_button_02.tga",
							"down_image": "d:/ymir work/ui/itemshop/category_button_03.tga",

							"text": "",
						},
						{
							"name": "category_button_08",
							"type": "radio_button",

							"x": 11,
							"y": 9 + 34 * 7,

							"default_image": "d:/ymir work/ui/itemshop/category_button_01.tga",
							"over_image": "d:/ymir work/ui/itemshop/category_button_02.tga",
							"down_image": "d:/ymir work/ui/itemshop/category_button_03.tga",

							"text": "",
						},
						{
							"name": "category_button_09",
							"type": "radio_button",

							"x": 11,
							"y": 9 + 34 * 8,

							"default_image": "d:/ymir work/ui/itemshop/category_button_01.tga",
							"over_image": "d:/ymir work/ui/itemshop/category_button_02.tga",
							"down_image": "d:/ymir work/ui/itemshop/category_button_03.tga",

							"text": "",
						},
						{
							"name": "category_button_10",
							"type": "radio_button",

							"x": 11,
							"y": 9 + 34 * 9,

							"default_image": "d:/ymir work/ui/itemshop/category_button_01.tga",
							"over_image": "d:/ymir work/ui/itemshop/category_button_02.tga",
							"down_image": "d:/ymir work/ui/itemshop/category_button_03.tga",

							"text": "",
						},
						{
							"name": "category_button_11",
							"type": "radio_button",

							"x": 11,
							"y": 9 + 34 * 10,

							"default_image": "d:/ymir work/ui/itemshop/category_button_01.tga",
							"over_image": "d:/ymir work/ui/itemshop/category_button_02.tga",
							"down_image": "d:/ymir work/ui/itemshop/category_button_03.tga",

							"text": "",
						},
						{
							"name": "category_button_12",
							"type": "radio_button",

							"x": 11,
							"y": 9 + 34 * 11,

							"default_image": "d:/ymir work/ui/itemshop/category_button_01.tga",
							"over_image": "d:/ymir work/ui/itemshop/category_button_02.tga",
							"down_image": "d:/ymir work/ui/itemshop/category_button_03.tga",

							"text": "",
						},
						{
							"name": "category_button_13",
							"type": "radio_button",

							"x": 11,
							"y": 9 + 34 * 12,

							"default_image": "d:/ymir work/ui/itemshop/category_button_01.tga",
							"over_image": "d:/ymir work/ui/itemshop/category_button_02.tga",
							"down_image": "d:/ymir work/ui/itemshop/category_button_03.tga",

							"text": "",
						},
					),
				},
				{
					"name": "money_thin",
					"type": "image",

					"x": 460,
					"y" : 11,

					"image" : "d:/ymir work/ui/itemshop/coins_slot.tga",

					"children" : (
						{
							"name": "money_value",
							"type": "text",

							"x": 0,
							"y": 0,

							"all_align": "center",

							"text": ""
						},
					),
				},

				{
					"name": "items_board",
					"type": "window",

					"x": 220,
					"y" : 90,

					"width" : 480,
					"height" : 413,

				},
			),
		},
	),
}