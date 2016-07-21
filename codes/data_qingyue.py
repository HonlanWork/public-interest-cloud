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
# 整理 青悦 国控空气检测站点分布数据
# 并存储到表qingyue_air_station中
# 197个站点
# '''
cursor.execute("delete from qingyue_air_station")

number = 0
fr = open('../data/上海青悦环保数据2/山东江苏空气监测站点基础数据.txt', 'r')
for line in fr:
	number += 1
	if number == 1:
		continue

	line = line.strip('\n').strip()
	line = line.split(',')

	cursor.execute("insert into qingyue_air_station(province, city, citycode, station, stationcode, lng, lat, reference) values(%s, %s, %s, %s, %s, %s, %s, %s)", [line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7]])

print number
fr.close()
# '''
##########################################

##########################################
# 整理 青悦 国控站点监测实时空气污染数据
# 并存储到表qingyue_air_data中
# 114063条记录
# '''
cursor.execute("delete from qingyue_air_data")

number = 0
fr = open('../data/上海青悦环保数据2/山东江苏201512空气监测数据.txt', 'r')
for line in fr:
	number += 1
	if number == 1:
		continue
	
	line = line.strip('\n').strip()
	line = line.split(',')

	cursor.execute("insert into qingyue_air_data(province, city, citycode, station, stationcode, aqi, level, main, so2, so2_24h, no2, no2_24h, co, co_24h, o3, o3_1h_max, o3_8h_ma, o3_8h_max, pm10, pm10_24h, pm25, pm25_24h, timestamp) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [line[1], line[2], line[3], line[5], line[6], line[7], line[8], line[10], line[-15], line[-14], line[-13], line[-12], line[-11], line[-10], line[-9], line[-8], line[-7], line[-6], line[-5], line[-4], line[-3], line[-2], str(int(time.mktime(time.strptime(line[-1], "%Y-%m-%d %H:%M:%S"))))])

print number
fr.close()
# '''
##########################################

##########################################
# 整理 青悦 国控地表水基础信息数据
# 并存储到表qingyue_water_station中
# 145个站点
# '''
cursor.execute("delete from qingyue_water_station")

number = 0
fr = open('../data/上海青悦环保数据2/国控地表水监测站基础信息.txt', 'r')
for line in fr:
	number += 1
	if number == 1:
		continue
	
	line = line.strip('\n').strip()
	line = line.split(',')

	if not line[8] == '':
		line[8] = str(int(time.mktime(time.strptime(line[8], "%Y年%m月"))))

	cursor.execute("insert into qingyue_water_station(stationno, station, flowarea, secpro, lng, lat, intro, org, timestamp, status) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9]])

print number
fr.close()
# '''
##########################################

##########################################
# 整理 青悦 国控地表水站点监测数据
# 并存储到表qingyue_water_data中
# 20581条记录
# '''
cursor.execute("delete from qingyue_water_data")

number = 0
fr = open('../data/上海青悦环保数据2/国控地表水201512站点监测数据.txt', 'r')
for line in fr:
	number += 1
	if number == 1:
		continue
	
	line = line.strip('\n').strip()
	line = line.split(',')

	cursor.execute("insert into qingyue_water_data(stationno, timestamp, ph, ph_level, o2, o2_level, nh4, nh4_level, kmno4, kmno4_level, c, c_level) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[line[0], str(int(time.mktime(time.strptime(line[1], "%Y-%m-%d %H:%M:%S")))), line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11]])

print number
fr.close()
# '''
##########################################

##########################################
# 整理 青悦 污染排放企业信息数据
# 并存储到表qingyue_pollution_company中
# 1193家企业
# '''
cursor.execute("delete from qingyue_pollution_company")

number = 0
fw = open('../data/上海青悦环保数据2/山东污染排放企业信息_clean.txt', 'w')
fr = open('../data/上海青悦环保数据2/山东污染排放企业信息.txt', 'r')
for line in fr:
	number += 1
	if number == 1:
		fw.write(line)
		continue
	
	line = line.strip('\n').strip()
	line = line.split(',')
	
	if len(line) == 27:
		for x in xrange(10, len(line) - 1):
			line[x] = line[x + 1]
		line = line[:-1]
		fw.write(','.join(line) + '\n')
	else:
		fw.write(','.join(line) + '\n')

	cursor.execute("insert into qingyue_pollution_company(companyid, companyname, orgcode, lawman, contacter, phone, pollutionname, pollutiontype, district, national, industry, address, lng, lat, lng_gd, lat_gd, lng_bd, lat_bd, timestamp, cycle, province, city, companyno, intro, originid, year) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17], str(int(time.mktime(time.strptime(line[-8], "%Y-%m-%d %H:%M:%S")))), line[-7], line[-6], line[-5], line[-4], line[-3], line[-2], line[-1]])

print number
fr.close()
fw.close()
# '''
##########################################

##########################################
# 整理 青悦 污染企业监测站点信息数据
# 并存储到表qingyue_pollution_station中
# 6641个站点
# '''
cursor.execute("delete from qingyue_pollution_station")

number = 0
fr = open('../data/上海青悦环保数据2/山东污染企业所属监测站点信息.txt', 'r')
for line in fr:
	number += 1
	if number == 1:
		continue
	
	line = line.strip('\n').strip()
	line = line.split(',')

	cursor.execute("insert into qingyue_pollution_station(stationid, companyid, stationname, isdelegated, timestamp) values(%s, %s, %s, %s, %s)",[line[0], line[1], line[4], line[8], str(int(time.mktime(time.strptime(line[-3], "%Y-%m-%d %H:%M:%S"))))])

print number
fr.close()
# '''
##########################################

##########################################
# 整理 青悦 污染企业监测站点监测项目信息数据
# 并存储到表qingyue_pollution_item中
# 3322条记录
# '''
cursor.execute("delete from qingyue_pollution_item")

number = 0
fr = open('../data/上海青悦环保数据2/山东污染企业监测站点所属监测项目信息.txt', 'r')
for line in fr:
	number += 1
	if number == 1:
		continue
	
	line = line.strip('\n').strip()
	line = line.split(',')

	cursor.execute("insert into qingyue_pollution_item(itemid, stationid, itemname, frequency, maxv, minv, source, means, beginday, timestamp) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], str(int(time.mktime(time.strptime(line[8], "%Y-%m-%d")))), str(int(time.mktime(time.strptime(line[9], "%Y-%m-%d %H:%M:%S"))))])

print number
fr.close()
# '''
##########################################

##########################################
# 整理 青悦 山东企业污染排放国控监测数据
# 并存储到表qingyue_pollution_data中
# 356697条记录
# '''
cursor.execute("delete from qingyue_pollution_data")

number = 0
fr = open('../data/上海青悦环保数据2/山东污染排放企业201512排放记录.txt', 'r')
for line in fr:
	number += 1
	if number == 1:
		continue
	
	line = line.strip('\n').strip()
	line = line.split(',')

	cursor.execute("insert into qingyue_pollution_data(stationid, itemname, frequency, itemid, value, timestamp, means, isover, overtype, overmultiple, save_timestamp, status, note, province, upper, lower, updatebool) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[line[1], line[2], line[3], line[4], line[5], str(int(time.mktime(time.strptime(line[6], "%Y-%m-%d %H:%M:%S")))), line[7], line[8], line[9], line[10], str(int(time.mktime(time.strptime(line[11], "%Y-%m-%d %H:%M:%S")))), line[12], line[13], line[14], line[15], line[16], line[17]])

print number
fr.close()
# '''
##########################################

cursor.close()
db.close()