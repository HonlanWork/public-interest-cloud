library(ggplot2)
library(gpclib)
library(maptools)
library(mapproj)

# 地图
map_line <- readShapePoly("maps/bou4/BOUNT_poly.shp")
Shandong <- fortify(map_line[substr(as.character(map_line$ADCODE99),1,2) == '37',])
names(Shandong)[1:2] <- c("经度", "纬度")
qingyue_pollution_company <- qingyue_pollution_company[qingyue_pollution_company$经度 >=114.8 & qingyue_pollution_company$经度 <= 122.7 & qingyue_pollution_company$纬度 >= 34.39 & qingyue_pollution_company$纬度 <= 38.41, ]
ggplot() + geom_polygon(data=Shandong, aes(x=经度, y=纬度, group=id), color="grey", fill=NA) + labs(title='污染_1_山东污染企业地理分布') + theme_grey() + coord_map() + geom_point(data=qingyue_pollution_company, aes(x=经度,y=纬度,color=市)) + labs(title='污染_1_山东污染企业地理分布') + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank())
ggplot() + geom_bar(data=qingyue_pollution_company, aes(x=市), stat="count") + labs(y='污染企业数量', title='污染_2_山东污染企业城市统计') + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank(), axis.text.x=element_text(angle=90))

link <- read.csv("link_stat.txt", sep=",", header=TRUE)
qingyue_pollution_company <- merge(qingyue_pollution_company, link)
rm(link)

ggplot(qingyue_pollution_company) + geom_abline(intercept=0, slope=1, linetype='dashed', alpha=.6) + geom_point(aes(x=监测站数量, y=监测项目数量, color=市), position=position_jitter(width=.5, height=.5), alpha=.6) + labs( title='污染_3_山东污染企业对应监测站数量和监测项目数量') + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank())
