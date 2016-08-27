# 空气站点
qingyue_air_station <- read.csv("../../data/上海青悦环保数据2/山东江苏空气监测站点基础数据.txt", sep=",", header=TRUE)
qingyue_air_station$城市编码 <- factor(qingyue_air_station$城市编码)
# 空气数据
qingyue_air_data <- read.csv("../../data/上海青悦环保数据2/山东江苏201512空气监测数据.txt", sep=",", header=TRUE)
qingyue_air_data$城市编码 <- factor(qingyue_air_data$城市编码)
qingyue_air_data$SO2 <- as.numeric(qingyue_air_data$SO2)
# 水质站点
qingyue_water_station <- read.csv("../../data/上海青悦环保数据2/国控地表水监测站基础信息.txt", sep=",", header=TRUE)
qingyue_water_station <- qingyue_water_station[, -7]
qingyue_water_station$编号 <- factor(qingyue_water_station$编号)
qingyue_water_station_Shandong <- qingyue_water_station[grep("山东", qingyue_water_station$名称),]
# 水质数据
qingyue_water_data <- read.csv("../../data/上海青悦环保数据2/国控地表水201512站点监测数据.txt", sep=",", header=TRUE)
qingyue_water_data$站点编号 <- factor(qingyue_water_data$站点编号)
# 污染企业
qingyue_pollution_company <- read.csv("../../data/上海青悦环保数据2/山东污染排放企业信息_clean.txt", sep=",", header=TRUE)
qingyue_pollution_company$企业ID <- factor(qingyue_pollution_company$企业ID)
qingyue_pollution_company$经度 <- as.numeric(qingyue_pollution_company$经度)
qingyue_pollution_company$原站ID <- factor(qingyue_pollution_company$原站ID)
qingyue_pollution_company$数据年份 <- factor(qingyue_pollution_company$数据年份)
# 污染站点
qingyue_pollution_station <- read.csv("../../data/上海青悦环保数据2/山东污染企业所属监测站点信息.txt", sep=",", header=TRUE)
qingyue_pollution_station$ID <- factor(qingyue_pollution_station$ID)
qingyue_pollution_station$污染企业ID <- factor(qingyue_pollution_station$污染企业ID)
# 污染项目
qingyue_pollution_item <- read.csv("../../data/上海青悦环保数据2/山东污染企业监测站点所属监测项目信息.txt", sep=",", header=TRUE)
qingyue_pollution_item$ID <- factor(qingyue_pollution_item$ID)
qingyue_pollution_item$监测站点ID <- factor(qingyue_pollution_item$监测站点ID)
# 污染数据
qingyue_pollution_data <- read.csv("../../data/上海青悦环保数据2/山东污染排放企业201512排放记录.txt", sep=",", header=TRUE)
qingyue_pollution_data$ID <- factor(qingyue_pollution_data$ID)
qingyue_pollution_data$监测点ID <- factor(qingyue_pollution_data$监测点ID)
qingyue_pollution_data$监测项目ID <- factor(qingyue_pollution_data$监测项目ID)

