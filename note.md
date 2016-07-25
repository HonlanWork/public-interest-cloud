## 数据资产
1. 中国天气网天气	2517个县级城市	22048920条记录	2015/1/1 0:0:0 ~ 2015/12/31 23:0:0
2. 中国天气网风场格点	221130条记录	2015/12/1 0:0:0 ~ 2015/12/30 0:0:0
3. 青悦空气监测数据	山东、江苏	197个站点	114063条记录，每个站点579条	2015/12/1 0:0:0 ~ 2015/12/31 23:0:0	
4. 青悦水质监测数据	全国	145个站点（143个处于中国范围内）	20581（19894，15562）条记录，每个站点142条	2015/12/1 0:0:0 ~ 2015/12/31 23:0:0	每4个小时一条
4. 青悦污染监测数据	1193家企业（1110家处于山东范围内）	6641个监测站点	3322个监测项目	356697条记录	2015/12/1 0:0:0 ~ 2015/12/31 23:0:0

# 地图
map_line <- readShapePoly("maps/bou4/BOUNT_poly.shp")
Shandong <- fortify(map_line[substr(as.character(map_line$ADCODE99),1,2) == '37',])
ShandongJiangsu <- fortify(map_line[substr(as.character(map_line$ADCODE99),1,2) == '37' | substr(as.character(map_line$ADCODE99),1,2) == '32',])
names(Shandong)[1:2] <- c("经度", "纬度")
names(ShandongJiangsu)[1:2] <- c("经度", "纬度")
# 空气监测站点分布
ggplot() + geom_polygon(data=ShandongJiangsu, aes(x=经度, y=纬度, group=id), color="grey", fill=NA) + theme_grey() + coord_map() + geom_point(data=qingyue_air_station, aes(x=经度,y=纬度,color=城市,shape=省份)) + labs(title='空气监测站点地理分布') + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank())
# 水质监测站点分布
ggplot() + geom_polygon(data=Shandong, aes(x=经度, y=纬度, group=id), color="grey", fill=NA) + theme_grey() + coord_map() + geom_point(data=qingyue_water_station_Shandong, aes(x=经度,y=纬度,color=所属流域)) + labs(title='水质监测站点地理分布') + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank())
# 污染企业分布
ggplot() + geom_polygon(data=Shandong, aes(x=经度, y=纬度, group=id), color="grey", fill=NA) + theme_grey() + coord_map() + geom_point(data=qingyue_pollution_company, aes(x=经度,y=纬度,color=市)) + labs(title='污染企业地理分布') + theme(text=element_text(family="Microsoft YaHei"), legend.title=element_blank())