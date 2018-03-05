CREATE TABLE `new_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL COMMENT '交易日期',
  `area` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '区域',
  `normal_trad_nm` decimal(20,2) DEFAULT NULL COMMENT '普通住宅成交数量',
  `normal_trad_vol` decimal(20,2) DEFAULT NULL COMMENT '普通住宅成交面积',
  `business_trad_nm` decimal(20,2) DEFAULT NULL COMMENT '商业成交数量',
  `business_trad_vol` decimal(20,2) DEFAULT NULL COMMENT '商业成交面积',
  `office_trad_nm` decimal(20,2) DEFAULT NULL COMMENT '写字楼成交数量',
  `office_trad_vol` decimal(20,2) DEFAULT NULL COMMENT '写字楼成交面积',
  `other_trad_nm` decimal(20,2) DEFAULT NULL COMMENT '其他成交数量',
  `toher_trad_vol` decimal(20,2) DEFAULT NULL COMMENT '其他成交面积',
  PRIMARY KEY (`id`),
  UNIQUE KEY `date_UNIQUE` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='date 日期，area 区域,normal_trad_nm'
