#!/usr/bin/env python
# coding:utf8

import time
import sys
reload(sys)
sys.setdefaultencoding( "utf8" )
from flask import *
import warnings
warnings.filterwarnings("ignore")
import MySQLdb
import MySQLdb.cursors
import numpy as np
from config import *
import pprint
import random

app = Flask(__name__)
app.config.from_object(__name__)

# 连接数据库
def connectdb():
	db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=DATABASE, port=PORT, charset=CHARSET, cursorclass = MySQLdb.cursors.DictCursor)
	db.autocommit(True)
	cursor = db.cursor()
	return (db,cursor)

# 关闭数据库
def closedb(db,cursor):
	db.close()
	cursor.close()

# 首页
@app.route('/')
def index():
	dataset = {}

	(db,cursor) = connectdb()

	cursor.execute("select * from json_data where keyword!=%s",['aqi_data_details'])
	
	json_data = cursor.fetchall()
	tmp = {}
	for item in json_data:
		tmp[item['keyword']] = json.loads(item['json'])
	dataset['json'] = tmp

	# 格式化aqi数据的时间戳
	timestamps = dataset['json']['aqi_data']['timestamps']
	tmp = []
	for item in timestamps:
		tmp.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(item))))
	dataset['json']['aqi_data']['timestamps'] = tmp

	# 空气监测站
	cursor.execute("select province, stationcode, lng, lat from qingyue_air_station")
	stations = cursor.fetchall()
	count_sd = 0
	count_js = 0
	tmp = {u'山东省':{}, u'江苏省':{}}
	for x in xrange(0, len(stations)):
		if stations[x]['province'] == u'山东省':
			count_sd += 1
		elif stations[x]['province'] == u'江苏省':
			count_js += 1
		tmp[stations[x]['province']][stations[x]['stationcode']] = [stations[x]['lng'], stations[x]['lat']]
	dataset['stations'] = tmp
	dataset['stations_count'] = {u'山东省':count_sd, u'江苏省':count_js}

	closedb(db,cursor)

	return render_template('index.html', dataset=json.dumps(dataset))

@app.route('/aqi_data_details', methods=['GET'])
def aqi_data_details():
	(db,cursor) = connectdb()

	cursor.execute("select * from json_data where keyword=%s",['aqi_data_details'])
	data = cursor.fetchone()['json']

	closedb(db,cursor)
	
	return data

# 天气
@app.route('/weather')
def weather():
	return render_template('weather.html')

# 水质
@app.route('/water')
def water():
	return render_template('water.html')

# 污染
@app.route('/pollution')
def pollution():
	return render_template('pollution.html')

if __name__ == '__main__':
	app.run(debug=True)