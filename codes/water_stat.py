#!/usr/bin/env python
# coding:utf8

import sys 
reload(sys)
sys.setdefaultencoding('utf8')
import MySQLdb
import MySQLdb.cursors
import time
import numpy as np
import json

db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='public-interest-cloud', port=8889, charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
db.autocommit(True)
cursor = db.cursor()

cursor.execute("select * from qingyue_water_data where ph>=0 and o2>=0 and nh4>=0 and kmno4>=0 and c>=0 and nh4!=9999")
water = cursor.fetchall()

cursor.execute("select * from qingyue_water_station where lng>=73.45 and lng<=135.09 and lat >= 6.319 and lat<=53.558 order by flowarea")
stations = cursor.fetchall()

rivers = {}
idx = 0

tmp = {}
for item in stations:
	tmp[item['stationno']] = item
stations = tmp
# 143
print len(stations)

# 各个站点各项指标平均值
tmp = {}
for item in water:
	if not tmp.has_key(item['stationno']):
		tmp[item['stationno']] = []
	tmp[item['stationno']].append(item)

water_point = []
amaxv = {'ph':0, 'o2':0, 'nh4':0, 'kmno4':0, 'c':0}
aminv = {'ph':999999, 'o2':999999, 'nh4':999999, 'kmno4':999999, 'c':999999}
maxv = {'ph':0, 'o2':0, 'nh4':0, 'kmno4':0, 'c':0}
minv = {'ph':999999, 'o2':999999, 'nh4':999999, 'kmno4':999999, 'c':999999}
for key, value in tmp.items():
	if not stations.has_key(key):
		continue
	t = {}
	for p in ['ph', 'o2', 'nh4', 'kmno4', 'c']:
		total = 0
		num = 0
		for item in value:
			if not rivers.has_key(stations[key]['flowarea']):
				rivers[stations[key]['flowarea']] = idx
				idx += 1

			if round(float(item[p]), 2) > maxv[p]:
				maxv[p] = round(float(item[p]), 2)
			if round(float(item[p]), 2) < minv[p]:
				minv[p] = round(float(item[p]), 2)

			total += float(item[p])
			num += 1
		t[p] = round(total / num, 2)
		t[p + '_num'] = num
		if round(float(t[p]), 2) > amaxv[p]:
			amaxv[p] = round(float(t[p]), 2)
		if round(float(t[p]), 2) < aminv[p]:
			aminv[p] = round(float(t[p]), 2)
	t['stationno'] = key
	t['flowarea'] = stations[key]['flowarea']
	t['flowarea_id'] = rivers[stations[key]['flowarea']]
	t['name'] = stations[key]['station']
	water_point.append(t)

print len(rivers)
print len(water)

cursor.execute("delete from json_data where keyword=%s",['water_point'])
cursor.execute("insert into json_data(keyword, json, page) values(%s, %s, %s)",['water_point', json.dumps({'max':amaxv,'min':aminv,'data':water_point,'rivers':rivers}), 'water'])

events = []
unique = []
# int(time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime(float(item['timestamp']))), "%Y-%m-%d")))
for item in water:
	if not stations.has_key(item['stationno']):
		continue

	if (float(item['ph']) - minv['ph']) / (maxv['ph'] - minv['ph']) >= 0.7:
		tmp = {'stationno': item['stationno'], 'date': time.strftime("%Y-%m-%d", time.localtime(float(item['timestamp']))), 'param': 'ph'}
		if not tmp in unique:
			unique.append(tmp)
			events.append({
				'stationno': item['stationno'],
				'station': stations[item['stationno']]['station'],
				'flowarea': stations[item['stationno']]['flowarea'],
				'lng': (float(stations[item['stationno']]['lng']) - 73.45) / (135.09 - 73.45),
				'lat': (float(stations[item['stationno']]['lat']) - 18.211) / (53.558 - 18.211),
				'timestamp': int(item['timestamp']),
				'date': time.strftime("%Y-%m-%d", time.localtime(float(item['timestamp']))),
				'param': 'PH值',
				'ratio': (float(item['ph']) - minv['ph']) / (maxv['ph'] - minv['ph']),
				'value': round(float(item['ph']), 2)
				});
	if (float(item['ph']) - minv['ph']) / (maxv['ph'] - minv['ph']) <= 0.3:
		tmp = {'stationno': item['stationno'], 'date': time.strftime("%Y-%m-%d", time.localtime(float(item['timestamp']))), 'param': 'ph'}
		if not tmp in unique:
			unique.append(tmp)
			events.append({
				'stationno': item['stationno'],
				'station': stations[item['stationno']]['station'],
				'flowarea': stations[item['stationno']]['flowarea'],
				'lng': (float(stations[item['stationno']]['lng']) - 73.45) / (135.09 - 73.45),
				'lat': (float(stations[item['stationno']]['lat']) - 18.211) / (53.558 - 18.211),
				'timestamp': int(item['timestamp']),
				'date': time.strftime("%Y-%m-%d", time.localtime(float(item['timestamp']))),
				'param': 'PH值',
				'ratio': (float(item['ph']) - minv['ph']) / (maxv['ph'] - minv['ph']),
				'value': round(float(item['ph']), 2)
				});
	if (float(item['o2']) - minv['o2']) / (maxv['o2'] - minv['o2']) >= 0.8:
		tmp = {'stationno': item['stationno'], 'date': time.strftime("%Y-%m-%d", time.localtime(float(item['timestamp']))), 'param': 'o2'}
		if not tmp in unique:
			unique.append(tmp)
			events.append({
				'stationno': item['stationno'],
				'station': stations[item['stationno']]['station'],
				'flowarea': stations[item['stationno']]['flowarea'],
				'lng': (float(stations[item['stationno']]['lng']) - 73.45) / (135.09 - 73.45),
				'lat': (float(stations[item['stationno']]['lat']) - 18.211) / (53.558 - 18.211),
				'timestamp': int(item['timestamp']),
				'date': time.strftime("%Y-%m-%d", time.localtime(float(item['timestamp']))),
				'param': '溶解氧',
				'ratio': (float(item['o2']) - minv['o2']) / (maxv['o2'] - minv['o2']),
				'value': round(float(item['o2']), 2)
				});
	if (float(item['o2']) - minv['o2']) / (maxv['o2'] - minv['o2']) <= 0.2:
		tmp = {'stationno': item['stationno'], 'date': time.strftime("%Y-%m-%d", time.localtime(float(item['timestamp']))), 'param': 'o2'}
		if not tmp in unique:
			unique.append(tmp)
			events.append({
				'stationno': item['stationno'],
				'station': stations[item['stationno']]['station'],
				'flowarea': stations[item['stationno']]['flowarea'],
				'lng': (float(stations[item['stationno']]['lng']) - 73.45) / (135.09 - 73.45),
				'lat': (float(stations[item['stationno']]['lat']) - 18.211) / (53.558 - 18.211),
				'timestamp': int(item['timestamp']),
				'date': time.strftime("%Y-%m-%d", time.localtime(float(item['timestamp']))),
				'param': '溶解氧',
				'ratio': (float(item['o2']) - minv['o2']) / (maxv['o2'] - minv['o2']),
				'value': round(float(item['o2']), 2)
				});
	if (float(item['nh4']) - minv['nh4']) / (maxv['nh4'] - minv['nh4']) >= 0.15:
		tmp = {'stationno': item['stationno'], 'date': time.strftime("%Y-%m-%d", time.localtime(float(item['timestamp']))), 'param': 'nh4'}
		if not tmp in unique:
			unique.append(tmp)
			events.append({
				'stationno': item['stationno'],
				'station': stations[item['stationno']]['station'],
				'flowarea': stations[item['stationno']]['flowarea'],
				'lng': (float(stations[item['stationno']]['lng']) - 73.45) / (135.09 - 73.45),
				'lat': (float(stations[item['stationno']]['lat']) - 18.211) / (53.558 - 18.211),
				'timestamp': int(item['timestamp']),
				'date': time.strftime("%Y-%m-%d", time.localtime(float(item['timestamp']))),
				'param': '氨氮',
				'ratio': (float(item['nh4']) - minv['nh4']) / (maxv['nh4'] - minv['nh4']),
				'value': round(float(item['nh4']), 2)
				});
	if (float(item['c']) - minv['c']) / (maxv['c'] - minv['c']) >= 0.1:
		tmp = {'stationno': item['stationno'], 'date': time.strftime("%Y-%m-%d", time.localtime(float(item['timestamp']))), 'param': 'c'}
		if not tmp in unique:
			unique.append(tmp)
			events.append({
				'stationno': item['stationno'],
				'station': stations[item['stationno']]['station'],
				'flowarea': stations[item['stationno']]['flowarea'],
				'lng': (float(stations[item['stationno']]['lng']) - 73.45) / (135.09 - 73.45),
				'lat': (float(stations[item['stationno']]['lat']) - 18.211) / (53.558 - 18.211),
				'timestamp': int(item['timestamp']),
				'date': time.strftime("%Y-%m-%d", time.localtime(float(item['timestamp']))),
				'param': '总有机碳',
				'ratio': (float(item['c']) - minv['c']) / (maxv['c'] - minv['c']),
				'value': round(float(item['c']), 2)
			});
timetexts = []
begintime = np.min([events[x]['timestamp'] for x in xrange(0, len(events))])
endtime = np.max([events[x]['timestamp'] for x in xrange(0, len(events))])
for x in xrange(0, 11):
	timetexts.append(time.strftime("%m-%d", time.localtime(float(begintime + x * (endtime - begintime) / 10))))

cursor.execute("delete from json_data where keyword=%s",['water_event'])
cursor.execute("insert into json_data(keyword, json, page) values(%s, %s, %s)",['water_event', json.dumps({'begintime': begintime, 'endtime': endtime, 'timetexts': timetexts, 'data': events}), 'water'])

cursor.close()
db.close()

