/*
 Navicat Premium Data Transfer

 Source Server         : 10.0.1.38_3306
 Source Server Type    : MySQL
 Source Server Version : 50634
 Source Host           : 10.0.1.38:3306
 Source Schema         : log

 Target Server Type    : MySQL
 Target Server Version : 50634
 File Encoding         : 65001

 Date: 19/08/2019 14:49:33
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for itemshop_log
-- ----------------------------
DROP TABLE IF EXISTS `itemshop_log`;
CREATE TABLE `itemshop_log`  (
  `account_id` int(11) NULL DEFAULT NULL,
  `vnum` int(11) NULL DEFAULT NULL,
  `count` int(11) NULL DEFAULT NULL,
  `price` int(11) NULL DEFAULT NULL,
  `id` int(11) NULL DEFAULT NULL,
  `category` int(11) NULL DEFAULT NULL,
  `channel` smallint(6) NULL DEFAULT NULL,
  `date` datetime(0) NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
