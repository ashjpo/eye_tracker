/*
Navicat MySQL Data Transfer

Source Server         : 127
Source Server Version : 50553
Source Host           : localhost:3306
Source Database       : eye_tracker

Target Server Type    : MYSQL
Target Server Version : 50553
File Encoding         : 65001

Date: 2020-10-22 12:42:13
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` char(150) DEFAULT NULL,
  `autoCreatedType` char(50) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `last_update_time` datetime DEFAULT NULL,
  `if_delete` tinyint(1) DEFAULT '0',
  `scene_version_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for cat_group
-- ----------------------------
DROP TABLE IF EXISTS `cat_group`;
CREATE TABLE `cat_group` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `cat_id` bigint(20) DEFAULT NULL,
  `name` char(150) DEFAULT NULL,
  `dynamicObjectsIds_json` longtext,
  `create_time` datetime DEFAULT NULL,
  `last_update_time` datetime DEFAULT NULL,
  `if_delete` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for dynamic_obj
-- ----------------------------
DROP TABLE IF EXISTS `dynamic_obj`;
CREATE TABLE `dynamic_obj` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `scene_version_id` bigint(20) DEFAULT NULL,
  `sdk_id_str` varchar(150) DEFAULT NULL,
  `name` varchar(150) DEFAULT NULL,
  `mesh_name` varchar(150) DEFAULT NULL,
  `scene_file_type` varchar(50) DEFAULT NULL,
  `latest_screenshot_location` text,
  `resource_folder_path` text,
  `resource_file_name_json` text,
  `create_time` datetime DEFAULT NULL,
  `last_update_time` datetime DEFAULT NULL,
  `if_delete` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for objective
-- ----------------------------
DROP TABLE IF EXISTS `objective`;
CREATE TABLE `objective` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) DEFAULT NULL,
  `des` text,
  `create_time` datetime DEFAULT NULL,
  `last_update_time` datetime DEFAULT NULL,
  `scene_version_id` bigint(20) DEFAULT NULL,
  `if_delete` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for objective_version
-- ----------------------------
DROP TABLE IF EXISTS `objective_version`;
CREATE TABLE `objective_version` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `objective_id` bigint(20) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `step_json` longtext,
  `create_time` datetime DEFAULT NULL,
  `last_update_time` datetime DEFAULT NULL,
  `if_delete` tinyint(1) DEFAULT '0',
  `version_number` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for organization
-- ----------------------------
DROP TABLE IF EXISTS `organization`;
CREATE TABLE `organization` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) DEFAULT NULL,
  `des` text,
  `org_account` varchar(150) DEFAULT NULL,
  `org_password` varchar(150) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `if_delete` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for participant
-- ----------------------------
DROP TABLE IF EXISTS `participant`;
CREATE TABLE `participant` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `participant_id` varchar(150) DEFAULT NULL,
  `session_ids_json` longtext,
  `org_id` bigint(20) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `if_delete` tinyint(1) DEFAULT '0',
  `participant_name` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for project
-- ----------------------------
DROP TABLE IF EXISTS `project`;
CREATE TABLE `project` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) DEFAULT NULL,
  `des` text,
  `project_key` text,
  `create_time` datetime DEFAULT NULL,
  `last_update_time` datetime DEFAULT NULL,
  `org_id` bigint(20) DEFAULT NULL,
  `image_location` text,
  `project_type` varchar(500) DEFAULT NULL,
  `prefix` varchar(50) DEFAULT NULL,
  `resource_folder_path` text,
  `if_hidden` tinyint(1) DEFAULT '0',
  `if_delete` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for scene
-- ----------------------------
DROP TABLE IF EXISTS `scene`;
CREATE TABLE `scene` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) DEFAULT NULL,
  `des` text,
  `create_time` datetime DEFAULT NULL,
  `last_update_time` datetime DEFAULT NULL,
  `sdk_id_str` varchar(150) DEFAULT NULL,
  `pro_id` bigint(20) DEFAULT NULL,
  `customer_id` bigint(20) DEFAULT NULL,
  `latest_screenshot_location` text,
  `resource_folder_path` text,
  `if_hidden` tinyint(1) DEFAULT '0',
  `if_public` tinyint(1) DEFAULT '0',
  `if_delete` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for scene_version
-- ----------------------------
DROP TABLE IF EXISTS `scene_version`;
CREATE TABLE `scene_version` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version_number` bigint(20) DEFAULT NULL,
  `scene_id` bigint(20) DEFAULT NULL,
  `scene_file_type` varchar(50) DEFAULT NULL,
  `sdk_version` varchar(50) DEFAULT NULL,
  `scale` double DEFAULT NULL,
  `mesh_name` text,
  `latest_screenshot_location` text,
  `resource_file_name_json` text,
  `resource_folder_path` text,
  `create_time` datetime DEFAULT NULL,
  `last_update_time` datetime DEFAULT NULL,
  `if_delete` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for session
-- ----------------------------
DROP TABLE IF EXISTS `session`;
CREATE TABLE `session` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `session_id` text,
  `data_ids_json` text,
  `scene_version_id` bigint(20) DEFAULT NULL,
  `session_name` text,
  `hmdtype` varchar(50) DEFAULT NULL,
  `detect_interval` double DEFAULT NULL,
  `formatversion` varchar(50) DEFAULT NULL,
  `userid` text,
  `event_type_json` longtext,
  `properties_json` longtext,
  `session_start_time` datetime DEFAULT NULL,
  `session_end_time` datetime DEFAULT NULL,
  `session_duration` bigint(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `if_delete` tinyint(1) DEFAULT '0',
  `geo_json` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `des` text,
  `user_account` varchar(150) DEFAULT NULL,
  `user_password` varchar(150) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `power_level` varchar(50) DEFAULT NULL,
  `org_id` bigint(20) DEFAULT NULL,
  `if_delete` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
