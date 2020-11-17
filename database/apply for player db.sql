/*
 Navicat Premium Data Transfer

 Source Server         : 10.0.1.38_3306
 Source Server Type    : MySQL
 Source Server Version : 50634
 Source Host           : 10.0.1.38:3306
 Source Schema         : player

 Target Server Type    : MySQL
 Target Server Version : 50634
 File Encoding         : 65001

 Date: 19/08/2019 14:49:49
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for itemshop_editors
-- ----------------------------
DROP TABLE IF EXISTS `itemshop_editors`;
CREATE TABLE `itemshop_editors`  (
  `name` varchar(32) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for itemshop_items
-- ----------------------------
DROP TABLE IF EXISTS `itemshop_items`;
CREATE TABLE `itemshop_items`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category` smallint(5) UNSIGNED NOT NULL DEFAULT 0,
  `vnum` int(11) NOT NULL,
  `price` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `count` smallint(3) NOT NULL,
  `socket0` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `socket1` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `socket2` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `socket3` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `socket4` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `socket5` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `attrtype0` tinyint(4) NOT NULL DEFAULT 0,
  `attrvalue0` smallint(6) NOT NULL DEFAULT 0,
  `attrtype1` tinyint(4) NOT NULL DEFAULT 0,
  `attrvalue1` smallint(6) NOT NULL DEFAULT 0,
  `attrtype2` tinyint(4) NOT NULL DEFAULT 0,
  `attrvalue2` smallint(6) NOT NULL DEFAULT 0,
  `attrtype3` tinyint(4) NOT NULL DEFAULT 0,
  `attrvalue3` smallint(6) NOT NULL DEFAULT 0,
  `attrtype4` tinyint(4) NOT NULL DEFAULT 0,
  `attrvalue4` smallint(6) NOT NULL DEFAULT 0,
  `attrtype5` tinyint(4) NOT NULL DEFAULT 0,
  `attrvalue5` smallint(6) NOT NULL DEFAULT 0,
  `attrtype6` tinyint(4) NOT NULL DEFAULT 0,
  `attrvalue6` smallint(6) NOT NULL DEFAULT 0,
  `fixed_count` tinyint(1) NOT NULL DEFAULT 1,
  `add_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `item_vnum_index`(`vnum`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Fixed;

SET FOREIGN_KEY_CHECKS = 1;
