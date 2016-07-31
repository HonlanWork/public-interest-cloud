library(ggplot2)
library(gpclib)
library(maptools)
library(mapproj)

# 地图
map_line <- readShapePoly("maps/bou4/BOUNT_poly.shp")
Shandong <- fortify(map_line[substr(as.character(map_line$ADCODE99),1,2) == '37',])
names(Shandong)[1:2] <- c("经度", "纬度")
qingyue_pollution_company <- qingyue_pollution_company[qingyue_pollution_company$经度 >=114.8 & qingyue_pollution_company$经度 <= 122.7 & qingyue_pollution_company$纬度 >= 34.39 & qingyue_pollution_company$纬度 <= 38.41, ]
ggplot() + geom_polygon(data=Shandong, aes(x=经度, y=纬度, group=id), color="grey", fill=NA) + labs(title='污染_1_山东污染企业地理分布') + theme_grey() + coord_map() + geom_point(data=qingyue_pollution_company, aes(x=经度,y=纬度,color=市)) + labs(title='污染企业地理分布') + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank())
ggplot() + geom_bar(data=qingyue_pollution_company, aes(x=市), stat="count") + labs(y='污染企业数量', title='污染_2_山东污染企业城市统计') + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank(), axis.text.x=element_text(angle=90))
