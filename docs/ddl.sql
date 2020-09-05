-- DDL
CREATE DATABASE `data_quality` /*!40100 DEFAULT CHARACTER SET utf8 */ ;


-- 程序账号
create user system@'127.0.0.1' identified by 'H5cT7yHB8_';
grant all PRIVILEGES on data_quality.* to 'system'@'127.0.0.1';
flush privileges;

use data_quality;

-- 检核规则库，作为每个新次检核的模板表
CREATE TABLE `check_result_template` (
  `id` int(11) NOT NULL COMMENT '排序用id',
  `company` varchar(100) DEFAULT NULL COMMENT '二级公司名或系统名(拼音)',
  `source_system` varchar(10) NOT NULL COMMENT '二级公司名或系统名(中文)',
  `check_item` varchar(100) DEFAULT NULL COMMENT '数据标准',
  `target_table` varchar(100) DEFAULT NULL COMMENT '目标表',
  `risk_market_item` varchar(2) DEFAULT NULL COMMENT '是否风险集市需要的指标',
  `problem_type` varchar(100) DEFAULT NULL COMMENT '问题分类',
  `check_sql` varchar(4000) DEFAULT NULL COMMENT '报送SQL',
  `problem_id` varchar(4000) DEFAULT NULL COMMENT '问题数据对应主键编号',
  `item_count` int(11) DEFAULT NULL COMMENT '报送数据量',
  `problem_count` int(11) DEFAULT NULL COMMENT '问题数据量',
  `problem_per` decimal(10,2) DEFAULT NULL,
  `db` varchar(30) DEFAULT NULL,
  `note` varchar(4000) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  `update_flag` varchar(2) DEFAULT 'N',
  `check_date` timestamp NULL DEFAULT NULL,
  `check_version` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`,`source_system`)
);


-- 记录检核操作的日志表
CREATE TABLE `check_execute_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company` varchar(30) NOT NULL,
  `execute_date` timestamp NOT NULL,
  `execute_user` varchar(30) NOT NULL,
  `db` varchar(100) DEFAULT NULL,
  `status` varchar(400) NOT NULL,
  PRIMARY KEY (`id`)
) ;


-- 源系统改造需求管理表
CREATE TABLE `source_system_demand` (
  `id` int(11) DEFAULT NULL,
  `company` varchar(10) DEFAULT NULL,
  `item_name` varchar(100) DEFAULT NULL,
  `demand_name` varchar(100) DEFAULT NULL,
  `demand_created` varchar(20) DEFAULT NULL,
  `quarter` varchar(10) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `row_created` timestamp NULL DEFAULT CURRENT_TIMESTAMP
);
-- Excel数据导入的sql详见 demand\insert_excel.sql


-- 数据标准记录明细表
CREATE TABLE `data_standard_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `std_id` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `name` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `en_name` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `business_definition` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `business_rule` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `std_source` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `data_type` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `data_format` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `code_rule` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `code_range` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `code_meaning` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `business_range` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `dept` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `system` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY (`id`) USING BTREE
) ;


-- 数据标准记录概述表
CREATE TABLE `data_standard_desc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY (`id`) USING BTREE
);


-- 数据标准目录表
CREATE TABLE `data_standard_index` (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `idx_id` int(11) DEFAULT NULL COMMENT '树节点id',
  `idx_pid` int(11) DEFAULT NULL COMMENT '树父节点id',
  `idx_name` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '树节点名',
  `is_open` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '树节点是否默认展开',
  PRIMARY KEY (`pk_id`) USING BTREE
) ;

-- 数据标准更新记录表
CREATE TABLE `data_standard_update_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `std_name` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '数据标准名',
  `username` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '操作者',
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `previous_version` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '上一版本的内容',
  PRIMARY KEY (`id`) USING BTREE
);


-- 日期维度表
-- 时期生成，执行utils/generate_dim_date.py
CREATE TABLE `dim_date` (
  `date` datetime DEFAULT NULL,
  `day_id` int(11) NOT NULL,
  `year` int(11) DEFAULT NULL,
  `month` int(11) DEFAULT NULL,
  `day` int(11) DEFAULT NULL,
  `quarter` int(11) DEFAULT NULL,
  `day_name` text,
  `weekofyear` bigint(20) DEFAULT NULL,
  `dayofyear` int(11) DEFAULT NULL,
  `daysinmonth` int(11) DEFAULT NULL,
  `dayofweek` int(11) DEFAULT NULL,
  `is_leap_year` tinyint(1) DEFAULT NULL,
  `is_month_end` tinyint(1) DEFAULT NULL,
  `is_month_start` tinyint(1) DEFAULT NULL,
  `is_quarter_end` tinyint(1) DEFAULT NULL,
  `is_quarter_start` tinyint(1) DEFAULT NULL,
  `is_year_end` tinyint(1) DEFAULT NULL,
  `is_year_start` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`day_id`)
);


-- 数据源记录表
CREATE TABLE `source_db_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company` varchar(10) DEFAULT NULL,
  `name` varchar(40) DEFAULT NULL,
  `alias` varchar(50) DEFAULT NULL,
  `connection_string` varchar(100) DEFAULT NULL,
  `ip` varchar(16) DEFAULT NULL,
  `user` varchar(32) DEFAULT NULL,
  `passwd` varchar(200) DEFAULT NULL,
  `db` varchar(32) DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  `db_type` varchar(32) DEFAULT NULL,
  `charset` varchar(10) DEFAULT NULL,
  `note` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
);


-- ETL源-目标表，用于血缘分析
CREATE TABLE `datacenter_mapping` (
  `subject_area` varchar(255) DEFAULT NULL,
  `mapping_name` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  `target` varchar(255) DEFAULT NULL
);