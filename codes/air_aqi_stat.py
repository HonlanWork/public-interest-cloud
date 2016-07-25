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

cursor.execute("select avg(aqi) as ave_aqi, stationcode, province from qingyue_air_data where aqi != 0  group by stationcode order by ave_aqi asc")
stations = cursor.fetchall()
stations = [[stations[x]['stationcode'], stations[x]['province']] for x in xrange(0, len(stations))]

cursor.execute("select * from qingyue_air_data where aqi != 0")
# cursor.execute("select * from qingyue_air_data")
airs = cursor.fetchall()

data = {}
timestamps = []

fw = open('air_aqi_stat.csv', 'w')

for item in airs:
	if not item['timestamp'] in timestamps:
		timestamps.append(item['timestamp'])
	if not data.has_key(item['stationcode']):
		data[item['stationcode']] = {}
	data[item['stationcode']][item['timestamp']] = float(item['aqi'])

# 579
print len(timestamps)

timestamps.sort(key=lambda x:int(x))
# endtime = np.max([float(timestamps[x]) for x in xrange(0, len(timestamps))])
# begintime = np.min([float(timestamps[x]) for x in xrange(0, len(timestamps))])
# n = int((endtime - begintime) / 3600)
# timestamps = [str(int(begintime + 3600 * x)) for x in xrange(0, n + 1)]

result = {}
result['timestamps'] = timestamps
result['data'] = {u'山东省':{}, u'江苏省':{}}

matrix = {u'山东省':[], u'江苏省':[]}

for r in xrange(0, len(stations)):
	key = stations[r][0]
	value = data[key]
	tmp = []
	for c in xrange(0, len(timestamps)):
		if value.has_key(timestamps[c]):
			tmp.append(str(value[timestamps[c]]))
		else:
			tmp.append('-1')
	fw.write(','.join(tmp) + '\n')

	result['data'][stations[r][1]][key] = tmp
	matrix[stations[r][1]].append(tmp)
fw.close()

# 时间序列，各个站点每个时间戳的aqi
cursor.execute("delete from json_data where keyword=%s",['aqi_data'])
cursor.execute("insert into json_data(keyword, json, page) values(%s, %s, %s)",['aqi_data', json.dumps(result), 'index'])

for key, value in matrix.items():
	tmp = []
	for c in xrange(0, len(value[0])):
		number = 0
		total = 0
		for r in xrange(0, len(value)):
			number += 1
			total += float(value[r][c])
		tmp.append(int(total / number))
	matrix[key] = tmp

# 山东、江苏每天的平均aqi
cursor.execute("delete from json_data where keyword=%s",['aqi_average'])
cursor.execute("insert into json_data(keyword, json, page) values(%s, %s, %s)",['aqi_average', json.dumps(matrix), 'index'])

# 各个站点各项指标平均值
tmp = {}
for item in airs:
	if not tmp.has_key(item['stationcode']):
		tmp[item['stationcode']] = []
	tmp[item['stationcode']].append(item)

stationstat = []
for key, value in tmp.items():
	t = []
	for p in ['aqi', 'so2', 'no2', 'co', 'o3', 'pm10', 'pm25']:
		total = 0
		num = 0
		for item in value:
			total += float(item[p])
			num += 1
		t.append(round(total / num, 2))
	t.append(value[0]['province'])
	t.append(key)
	stationstat.append(t)

cursor.execute("delete from json_data where keyword=%s",['aqi_average_station'])
cursor.execute("insert into json_data(keyword, json, page) values(%s, %s, %s)",['aqi_average_station', json.dumps(stationstat), 'index'])

# 各个站点的详细数据
tmp = []
for x in xrange(0, 6):
	t = float(timestamps[0]) + x * (float(timestamps[-1]) - float(timestamps[0])) / 5
	t = time.strftime('%Y-%m-%d', time.localtime(t))
	tmp.append(t[2:])
details = {}
details['timestamps'] = timestamps
details['timetexts'] = tmp
details['data'] = {}
tmp = {}
for item in airs:
	if not tmp.has_key(item['stationcode']):
		tmp[item['stationcode']] = {}
	tmp[item['stationcode']][item['timestamp']] = item
for p in ['aqi', 'so2', 'no2', 'co', 'o3', 'pm10', 'pm25']:
	details['data'][p] = {}
	for key, value in tmp.items():
		t = []
		for c in xrange(0, len(timestamps)):
			if value.has_key(timestamps[c]):
				t.append(float(value[timestamps[c]][p]))
			else:
				t.append(0.0)
		details['data'][p][key] = t
	t = []
	maxv = -1
	for item in stations:
		t.append([item[0], item[1], details['data'][p][item[0]]])
		if np.max(details['data'][p][item[0]]) > maxv:
			maxv = np.max(details['data'][p][item[0]])
	mapping = []
	for x in xrange(0, len(t)):
		data = t[x][2]
		result = []
		# result.append([round(0.4 * float(x) / (len(t) - 1), 4), round(1 - 0.9 * float(x) / (len(t) - 1), 4)])
		for y in xrange(0, len(data)):
			if not y % 4 == 0:
				continue
			result.append([round(0.4 * float(x) / (len(t) - 1) + 0.6 * float(y) / (len(data) - 1), 4), round(1 - 0.9 * float(x) / (len(t) - 1) - 0.1 * float(data[y]) / maxv, 4)])
		# result.append([round(0.6 + 0.4 * float(x) / (len(t) - 1), 4), round(1 - 0.9 * float(x) / (len(t) - 1), 4)])
		mapping.append([t[x][0], t[x][1], result])
	details['data'][p] = [maxv, mapping]

cursor.execute("delete from json_data where keyword=%s",['aqi_data_details'])
cursor.execute("insert into json_data(keyword, json, page) values(%s, %s, %s)",['aqi_data_details', json.dumps(details), 'index'])

cursor.close()
db.close()