library(ggplot2)
library(gpclib)
library(maptools)
library(mapproj)

# 地图
map_line <- readShapePoly("maps/bou4/BOUNT_poly.shp")
ShandongJiangsu <- fortify(map_line[substr(as.character(map_line$ADCODE99),1,2) == '37' | substr(as.character(map_line$ADCODE99),1,2) == '32',])
names(ShandongJiangsu)[1:2] <- c("经度", "纬度")
# 空气监测站点分布
ggplot() + geom_polygon(data=ShandongJiangsu, aes(x=经度, y=纬度, group=id), color="grey", fill=NA) + theme_grey() + coord_map() + geom_point(data=qingyue_air_station, aes(x=经度,y=纬度,color=城市,shape=省份)) + labs(title='空气监测站点地理分布') + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank())
# AQI历史数据折线图
qingyue_air_data <- qingyue_air_data[qingyue_air_data$省份!='',]
qingyue_air_data$发布时间 <- as.POSIXct(qingyue_air_data$发布时间, format="%Y-%m-%d %H:%M:%S")
ggplot(data=qingyue_air_data) + geom_line(aes(x=发布时间, y=AQI)) + theme_grey() + facet_grid(省份~.) + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank())
# AQI历史数据一维密度图和二维密度图
ggplot(data=qingyue_air_data) + geom_density(aes(x=AQI)) + theme_grey() + facet_grid(省份~.) + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank())
ggplot(data=qingyue_air_data, aes(x=发布时间, y=AQI)) + stat_density2d(aes(fill = ..level..), geom="polygon") + scale_fill_continuous(high='darkblue',low='white') + facet_grid(省份~.) + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank())
