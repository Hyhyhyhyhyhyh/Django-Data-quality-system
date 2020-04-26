--DDL
CREATE DATABASE `data_quality` /*!40100 DEFAULT CHARACTER SET utf8 */ ;

--程序账号
create user system@'127.0.0.1' identified by '';
grant all PRIVILEGES on data_quality.* to 'system'@'127.0.0.1';
flush privileges;

--检核规则库，作为每个新季度的检核模板表
CREATE TABLE check_result_template (
  `id` int(11) NOT NULL COMMENT '排序用id',
  `source_system` varchar(10) NOT NULL COMMENT '二级公司名或系统名',
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
  PRIMARY KEY (`id`,`source_system`)
);

alter table check_result_template add (update_flag varchar(2) default 'N');

--记录检核操作的日志表，也用于下拉框选择季度用
create table check_execute_log(
    id int not null primary key auto_increment,
    quarter varchar(30) not null      COMMENT '检核的季度',
    company varchar(30) not null      COMMENT '检核的公司',
    execute_date date not null        COMMENT '完成检核的日期',
    execute_user varchar(30) not null COMMENT '执行检核的账号'
);
insert into check_execute_log values(null,'2019Q1','ycxt','2019-06-01','huangyiheng');
insert into check_execute_log values(null,'2019Q1','yczc','2019-06-01','huangyiheng');
insert into check_execute_log values(null,'2019Q1','gdzdb','2019-06-01','huangyiheng');
insert into check_execute_log values(null,'2019Q1','ycjk','2019-06-01','huangyiheng');
insert into check_execute_log values(null,'2019Q1','fdct','2019-06-01','huangyiheng');
insert into check_execute_log values(null,'2019Q1','zyyc','2019-06-01','huangyiheng');
insert into check_execute_log values(null,'2019Q1','jz','2019-06-01','huangyiheng');

insert into check_execute_log values(null,'2019Q2','ycxt','2019-07-01','huangyiheng');
insert into check_execute_log values(null,'2019Q2','yczc','2019-07-01','huangyiheng');
insert into check_execute_log values(null,'2019Q2','gdzdb','2019-07-01','huangyiheng');
insert into check_execute_log values(null,'2019Q2','ycjk','2019-07-01','huangyiheng');
insert into check_execute_log values(null,'2019Q2','fdct','2019-07-01','huangyiheng');
insert into check_execute_log values(null,'2019Q2','zyyc','2019-07-01','huangyiheng');
insert into check_execute_log values(null,'2019Q2','jz','2019-07-01','huangyiheng');


--源系统改造需求管理表
create table source_system_demand(
    id              int,
    company         varchar(10),
    item_name       varchar(100),
    demand_name     varchar(100),
    demand_created  varchar(20),
    quarter         varchar(10),
    status          varchar(100),
    row_created     timestamp DEFAULT current_timestamp()
);
--Excel数据导入的sql详见 demand\insert_excel.sql


--数据标准记录明细表
create table data_standard(
    id                  int auto_increment primary key,
    std_id              text,
    name                text,
    en_name             text,
    business_definition text,
    business_rule       text,
    std_source          text,
    data_type           text,
    data_format         text,
    code_rule           text,
    code_range          text,
    code_meaning        text,
    business_range      text,
    dept                text,
    `system`              text
);

--数据标准记录概述表
create table data_standard_desc(
	id int auto_increment primary key,
	name text,
	content text
);

-- 日期维度表
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