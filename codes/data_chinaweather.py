#!/usr/bin/env python
# coding:utf8

import sys 
reload(sys)
sys.setdefaultencoding('utf8')
import os
import os.path
import MySQLdb
import MySQLdb.cursors
import time

db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='public-interest-cloud', port=8889, charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
db.autocommit(True)
cursor = db.cursor()

##########################################
# 整理 中国天气网 全国县级城市实时天气数据
# 并存储到表chinaweather中
# 2517个县级城市
# 22048920条记录
# 2015/1/1 0:0:0 ~ 2015/12/31 23:0:0
# '''
cursor.execute("delete from chinaweather")

areas = []
number = 0
for parent, dirnames, filenames in os.walk('/Users/honlan/Desktop/git/public-interest-cloud/data/中国气象数据/chinaweather_station_observation/'):
	for filename in filenames:
		fr = open(parent + filename, 'r')

		if not filename.split('.')[0] in areas:
			areas.append(filename.split('.')[0])

		filename = filename.split('.')[0].split('_')

		for line in fr:
			line = line.strip().split(',')
			
			if line[0] == 'date':
				continue

			number += 1
			cursor.execute("insert into chinaweather(area1, area2, area3, timestamp, temp, rh, rain, windD, windP) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)", [filename[0], filename[1], filename[2], str(int(time.mktime(time.strptime(line[0].strip(), "%Y%m%d%H")))), line[1].strip(), line[2].strip(), line[3].strip(), line[4].strip(), line[5].strip()])

		fr.close()

print len(areas)
print number
# '''
##########################################

##########################################
# 整理 中国天气网 全国风场格点实况数据
# 并存储到表chinawind中
# 221130条记录
# 2015/12/1 0:0:0 ~ 2015/12/30 0:0:0
# '''
cursor.execute("delete from chinawind")

number = 0
fr = open('../data/中国气象数据2/全国风场格点201512实况数据.txt', 'r')
for line in fr:
	number += 1

	line = line.strip('\n').strip().decode('utf8')
	line = line.split(',')
	if number == 1:
		line[0] = line[0][1:]

	cursor.execute("insert into chinawind(timestamp, lng, lat, windD, windP) values(%s, %s, %s, %s, %s)", [str(int(time.mktime(time.strptime(line[0], "%Y%m%d")))), line[1], line[2], line[3], line[4]])

print number
fr.close()
# '''
##########################################

cursor.close()
db.close()