/*
 Navicat Premium Data Transfer

 Source Server         : auto contact minkai
 Source Server Type    : MySQL
 Source Server Version : 80032
 Source Host           : localhost:3307
 Source Schema         : auto_db

 Target Server Type    : MySQL
 Target Server Version : 80032
 File Encoding         : 65001

 Date: 23/08/2025 14:39:31
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bl_groups
-- ----------------------------
DROP TABLE IF EXISTS `bl_groups`;
CREATE TABLE `bl_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of bl_groups
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for black_lists
-- ----------------------------
DROP TABLE IF EXISTS `black_lists`;
CREATE TABLE `black_lists` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `reason` text,
  `bl_group_id` int DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2250554 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of black_lists
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for company_name_histories
-- ----------------------------
DROP TABLE IF EXISTS `company_name_histories`;
CREATE TABLE `company_name_histories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `company_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `status` int DEFAULT NULL,
  `company_url` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `created_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `job_index` int DEFAULT NULL,
  `error_message` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=79680 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of company_name_histories
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for job_histories
-- ----------------------------
DROP TABLE IF EXISTS `job_histories`;
CREATE TABLE `job_histories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `contact_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `status` int DEFAULT '0',
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  `job_index` int DEFAULT NULL,
  `error_message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `process_time` float DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `setting_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1807368 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of job_histories
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for setting
-- ----------------------------
DROP TABLE IF EXISTS `setting`;
CREATE TABLE `setting` (
  `id` int NOT NULL AUTO_INCREMENT,
  `company_name` varchar(255) DEFAULT NULL,
  `department` varchar(255) DEFAULT NULL,
  `lastname` varchar(100) DEFAULT NULL,
  `firstname` varchar(100) DEFAULT NULL,
  `lastname_kana` varchar(100) DEFAULT NULL,
  `firstname_kana` varchar(100) DEFAULT NULL,
  `fax` varchar(50) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `company_url` varchar(255) DEFAULT NULL,
  `number_of_employees` int DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `zip` varchar(20) DEFAULT NULL,
  `zip1` varchar(10) DEFAULT NULL,
  `zip2` varchar(10) DEFAULT NULL,
  `province` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `address` text,
  `title_question` varchar(255) DEFAULT NULL,
  `content_question` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name_of_setting` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of setting
-- ----------------------------
BEGIN;
INSERT INTO `setting` (`id`, `company_name`, `department`, `lastname`, `firstname`, `lastname_kana`, `firstname_kana`, `fax`, `email`, `company_url`, `number_of_employees`, `phone`, `zip`, `zip1`, `zip2`, `province`, `city`, `address`, `title_question`, `content_question`, `created_at`, `updated_at`, `name_of_setting`) VALUES (25, 'ソーシャルワイヤー株式会社', '', '小暮', '', 'コグレ', '', '03-5363-4871', 'support@atpress.ne.jp', 'https://www.atpress.ne.jp/', 500, '03-6868-0465', '1050004', '105', '0004', '東京都', '港区新橋', '1-1-13 ', '【サービス統合によるご面談の日程調整】＠Press/NEWSCAST', '平素よりお世話になっております。\n＠Press/NEWSCAST運営事務局の小暮です。\n\n日頃より弊社のサービスをご利用いただき誠にありがとうございます！\n\n8月4日（月）に「＠Press」と姉妹サービス「NEWSCAST」が統合することになりました。\n＠Pressでは一部プラン内容の見直しが行われますので、新サービスなども併せてご説明のお時間を\nいただければと思い、ご連絡させていただきました。\n\nお打合せいただいた方限定の特別料金でのご案内も可能です。\n年内にプレスリリースをご予定されている場合は、今後のご案内もさせていただければと存じます。\n\nお手すきの際に20分ほどお打ち合わせのお時間いただくことは可能でしょうか。\n面談可能時間　（前回の配信結果も振り返り可能）\n■7月16日（水曜日）　10:00～17:00\n■7月17日（木曜日）　10:00～17:00\n■7月18日（金曜日）　10:00～17:00\n\n＊上記以外でも下記のリンクよりご予約が可能です。\nhttps://timerex.net/s/ck235577_2312/a8c449b6/\n\n今後もよりご希望に沿ったプレスリリースができるようご尽力させていただければと存じます。ご返信のほどお待ちしております！', '2025-07-16 10:23:30', '2025-07-16 10:23:30', '【NCアポ＿小暮】');
INSERT INTO `setting` (`id`, `company_name`, `department`, `lastname`, `firstname`, `lastname_kana`, `firstname_kana`, `fax`, `email`, `company_url`, `number_of_employees`, `phone`, `zip`, `zip1`, `zip2`, `province`, `city`, `address`, `title_question`, `content_question`, `created_at`, `updated_at`, `name_of_setting`) VALUES (26, 'ソーシャルワイヤー株式会社', '', '小暮', '', 'コグレ', '', '03-5363-4871', 'support@atpress.ne.jp', 'https://www.atpress.ne.jp/', 500, '03-6868-0465', '1050004', '105', '0004', '東京都', '港区新橋', '1-1-13 ', '【サービス統合によるご面談の日程調整】＠Press/NEWSCAST', '平素よりお世話になっております。\n＠Press/NEWSCAST運営事務局の小暮です。\n\n日頃より弊社のサービスをご利用いただき誠にありがとうございます！\n\n8月4日（月）に「＠Press」と姉妹サービス「NEWSCAST」が統合することになりました。\n＠Pressでは一部プラン内容の見直しが行われますので、新サービスなども併せてご説明のお時間を\nいただければと思い、ご連絡させていただきました。\n\nお打合せいただいた方限定の特別料金でのご案内も可能です。\n年内にプレスリリースをご予定されている場合は、今後のご案内もさせていただければと存じます。\n\nお手すきの際に20分ほどお打ち合わせのお時間いただくことは可能でしょうか。\n面談可能時間　（前回の配信結果も振り返り可能）\n■7月16日（水曜日）　10:00～17:00\n■7月17日（木曜日）　10:00～17:00\n■7月18日（金曜日）　10:00～17:00\n\n＊上記以外でも下記のリンクよりご予約が可能です。\nhttps://timerex.net/s/ck235577_2312/a8c449b6/\n\n今後もよりご希望に沿ったプレスリリースができるようご尽力させていただければと存じます。ご返信のほどお待ちしております！', NULL, NULL, '【NCアポ＿小暮】');
COMMIT;

-- ----------------------------
-- Table structure for upload_histories
-- ----------------------------
DROP TABLE IF EXISTS `upload_histories`;
CREATE TABLE `upload_histories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `file_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `number_of_records` int DEFAULT NULL,
  `status` int DEFAULT NULL,
  `created` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `file_path_result` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of upload_histories
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
