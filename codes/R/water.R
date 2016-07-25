library(ggplot2)
library(gpclib)
library(maptools)
library(mapproj)

# 地图
map_line <- readShapePoly("maps/bou2/bou2_4p.shp")
China <- fortify(map_line)
names(China)[1:2] <- c("经度", "纬度")
# 水质监测站点分布
qingyue_water_station <- qingyue_water_station[qingyue_water_station$经度 >=73.45 & qingyue_water_station$经度 <= 135.09 & qingyue_water_station$纬度 >= 6.319 & qingyue_water_station$纬度 <= 53.558, ]
ggplot() + geom_polygon(data=China, aes(x=经度, y=纬度, group=id), color="grey", fill=NA) + theme_grey() + coord_map() + geom_point(data=qingyue_water_station, aes(x=经度,y=纬度,color=所属流域)) + labs(title='水质监测站点地理分布') + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank())

qingyue_water_data <- qingyue_water_data[qingyue_water_data$PH值>=0 & qingyue_water_data$溶解氧>=0 & qingyue_water_data$氨氮>=0 & qingyue_water_data$高锰酸盐>=0 & qingyue_water_data$总有机碳>=0,]
qingyue_water_data$时间 <- as.POSIXct(qingyue_water_data$时间, format="%Y-%m-%d %H:%M:%S")
ggplot(data=qingyue_water_data) + geom_line(aes(x=时间, y=PH值)) + theme_grey() + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank())

ggplot(data=qingyue_water_data) + geom_boxplot(aes(x=站点编号, y=PH值)) + theme_grey() + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank())
ggplot(data=qingyue_water_data) + geom_density(aes(x=PH值)) + theme_grey() + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank())
ggplot(data=qingyue_water_data, aes(x=时间, y=PH值)) + stat_density2d(aes(fill = ..level..), geom="polygon") + scale_fill_continuous(high='darkblue',low='white') + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank())

