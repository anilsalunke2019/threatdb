# -*- coding: utf-8 -*-
"""
Main API views implementation
Created on 21/10/2019
@author: Anurag
"""

# imports
import os
import json
from datetime import datetime

import requests
from flask import Flask, request, jsonify
from mysql.connector import connect

# local imports
from api.models import BlockedIPsModel, MalwareURLsModel, AuthDataModel, RevisionTrackerModel, db
from api.authenticator import Authenticator
from common.config import conf

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = conf.read().get('db-conf', 'DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
auth = Authenticator(request)


@app.route('/', methods=['GET'])
def home():
    """
    A index api view
    :return:
    """
    host = request.host_url
    response = {
        'message': 'Welcome to threat hub API service',
        'api_list': {
            1: host + 'api/register',
            2: host + 'api/ip/list',
            3: host + 'api/ip/list?revision=',
            4: host + 'api/ip/search?ip=',
            5: host + 'api/url/list',
            6: host + 'api/url/list?threat_type=phishing',
            7: host + 'api/url/list?threat_type=malware',
            8: host + 'api/url/list?threat_type=ransomware',
            9: host + 'api/url/list?domain=',
            10: host + 'api/url/list?filename=',
            11: host + 'api/url/search?url=',
            12: host + 'api/threats/top/<count>',
            13: host + 'api/alarm/alerts',
        }
    }
    return jsonify(response), 200


@app.route('/api/register', methods=['GET'])
def sign_up():
    """
    A Registration API to get access key
    :return:
    """
    client_ip = auth.get_remote_ip()
    all_ips = AuthDataModel.query.with_entities(AuthDataModel.client_ip).all()
    all_ips = [ip for tup in all_ips for ip in tup]
    if client_ip not in all_ips:
        return jsonify({'message': 'Unauthorised access'}), 401
    existed_record = AuthDataModel.query.filter_by(client_ip=client_ip).first()
    if existed_record and existed_record.api_key is None:
        token = auth.create_token(identity=client_ip)
        existed_record.api_key = token
        db.session.commit()
        result = jsonify({'message': "Registered successfully", 'access_key': token.decode()}), 200
        return result
    elif existed_record.client_ip == client_ip:
        return jsonify({'message': 'Already registered', 'access_key': existed_record.api_key}), 200
    else:
        return jsonify({'message': 'Error occurred'}), 500


@app.route('/api/ip/list', methods=['GET'])
@auth.token_required
def get_iplist():
    """
    API for accessing all ip address data
    format: /ip/list
    format: /ip/list?revision=
    :return: json response
    """
    if not request.args:
        all_ip = BlockedIPsModel.query.all()
        return jsonify({"count": len(all_ip), "result": [i.serialize for i in all_ip]}), 200
    else:
        rev = int(request.args.get('revision'))
        nex_rev = int(rev) + 1
        last_revision = RevisionTrackerModel.query.get(1).last_revision
        if rev > last_revision:
            return jsonify({"message": "invalid revision", "latest_revision": last_revision, 'count': 0}), 400
        else:
            result = BlockedIPsModel.query.filter_by(revision=nex_rev).all()
            if not len(result) == 0:
                return jsonify({"count": len(result), "result": [i.serialize for i in result]}), 200
        return jsonify({"count": len(result), "result": "Database is up to date"}), 200


@app.route('/api/ip/search', methods=['GET'])
@auth.token_required
def search_ip():
    """
    API for accessing single ip information if it is present
    format : /ip/search?ip=
    :return: json response
    """
    req = request.args.get('ip', None)
    if req:
        ip = BlockedIPsModel.query.filter_by(ip_address=req).first()
        if not ip:
            return jsonify({"message": "Not found"}), 404
        return jsonify({"count": 1, "result": ip.serialize}), 200
    else:
        return jsonify({"message": "Bad query"}), 400


@app.route('/api/url/search', methods=['GET'])
@auth.token_required
def search_url():
    """
    API for accessing single url information if it is present
    format : /url/search?url=http:www.google.com
    :return:
    """
    req = request.args
    if 'url' not in req.keys():
        return jsonify({'message': "Bad query"}), 400
    else:
        query = request.args.get('url')
        url = MalwareURLsModel.query.filter_by(url=query).first()
        if not url:
            return jsonify({'message': "Not found"}), 404
        return jsonify({"success": url.serialize}), 200


@app.route('/api/url/list', methods=['GET'])
@auth.token_required
def url_list():
    """
    API for getting url list based on different query strings
    :return:
    """
    query = request.args
    if not query:
        all_urls = MalwareURLsModel.query.all()
        return jsonify({"count": len(all_urls), 'result': [i.serialize for i in all_urls]}), 200
    if query:
        threat_type = request.args.get('threat_type', None)
        domain = request.args.get('domain', None)
        filename = request.args.get('filename', None)
        if threat_type:
            by_type = MalwareURLsModel.query.filter_by(threat_type=threat_type).all()
            if not by_type:
                return jsonify({'message': "Not found"}), 404
            return jsonify({"count": len(by_type), "success": [i.serialize for i in by_type]}), 200
        elif domain:
            by_domain = MalwareURLsModel.query.filter(MalwareURLsModel.domain.ilike('%' + domain + '%')).all()
            if not by_domain:
                return jsonify({'message': "Not found"}), 404
            return jsonify({"count": len(by_domain), 'result': [i.serialize for i in by_domain]}), 200
        elif filename:
            by_filename = MalwareURLsModel.query.filter(MalwareURLsModel.filename.ilike(filename)).all()
            if not by_filename:
                return jsonify({'message': "Not found"}), 404
            return jsonify({"count": len(by_filename), 'result': [i.serialize for i in by_filename]}), 200
        else:
            return jsonify({'message': "Bad query"}), 400


@app.route('/api/threats/top/<count>/', methods=['GET'])
def top_threats(count):
    """
    API for getting top threats
    """
    count = int(count)
    if count > 10:
        count = 10
    url = "https://api.metadefender.com/v4/feed/infected/"
    header = {"apikey": conf.read().get('Alexa', 'apikey')}
    response = requests.get(url=url, headers=header)
    response = json.loads(response.text)
    response = json.dumps(response['top_infected'][:count])
    list_response = json.loads(response)

    for dic in list_response:
        threat_name = "Not available"
        threat_type = None
        if dic['scan_results']['threat_name'] is not None:
            threat_type = dic['scan_results']['threat_name'].split('/')[0]
            threat_name = dic['scan_results']['threat_name'].split('/')[1]
        else:
            threat_type = dic['file_type_extension']
            dic['threat_type'] = threat_type
            dic['threat_name'] = threat_name
            del dic['scan_results']
    final_response = json.dumps(list_response)
    return final_response


@app.route('/api/alarm/alerts', methods=['GET'])
def current_threats():
    now = datetime.now()
    curr_time = now.strftime("%Y-%m-%d %H:%M:%S")
    USER = conf.read().get('SIEM-CONF', 'USER')
    PASSWORD = conf.read().get('SIEM-CONF', 'PASSWORD')
    HOST = conf.read().get('SIEM-CONF', 'HOST')
    DB_NAME = conf.read().get('SIEM-CONF', 'DB_NAME')

    if os.path.isfile('/home/threat-intelligent-hub/alexa_files/timestamp.txt'):
        tmp = open('/home/threat-intelligent-hub/alexa_files/timestamp.txt', 'r+')
        last_read = tmp.read()
        tmp.close()
        tmp = open('/home/threat-intelligent-hub/alexa_files/timestamp.txt', 'w+')
    else:
        tmp = open('/home/threat-intelligent-hub/alexa_files/timestamp.txt', 'w+')
        last_read = None

    conn = connect(user=USER, password=PASSWORD, host=HOST, database=DB_NAME)
    cursor = conn.cursor()
    query_first = "SELECT A.*,B.name FROM (SELECT inet6_ntoa(src_ip),inet6_ntoa(dst_ip),plugin_sid,risk,cast(timestamp as char) timestamp FROM alarm WHERE DATE(TIMESTAMP) = DATE(NOW() ))  A INNER JOIN plugin_sid B ON A.plugin_sid = B.sid  where A.risk >= 3  order by A.risk,A.timestamp desc  limit 10;"
    query_last = "SELECT A.src_ip,A.dst_ip,A.plugin_sid,A.risk,A.timestamp,B.name FROM  (SELECT inet6_ntoa(src_ip) as src_ip,inet6_ntoa(dst_ip) as dst_ip,plugin_sid,risk,cast(timestamp as char) timestamp,plugin_id  FROM alarm WHERE  timestamp between  CONVERT_TZ('{0}' , @@session.time_zone, '+00:00')  and   CONVERT_TZ( '{1}', @@session.time_zone, '+00:00') and  risk >= 3 )   A INNER JOIN plugin_sid B ON A.plugin_sid = B.sid  and B.plugin_id = A.plugin_id inner join  plugin C ON C.id = B.plugin_id order by A.risk desc ,A.timestamp desc  limit 10;".format(
        last_read, curr_time)

    if not last_read:
        cursor.execute(query_first)
        tmp.write(str(curr_time))
    else:
        cursor.execute(query_last)
        tmp.write(str(curr_time))
    # fields = [x[0] for x in cursor.description]  # this will extract row headers
    result = cursor.fetchall()
    len_data = len(result)
    json_dict = {}
    data = []
    formatted_date = ''
    if last_read:
        date_time_obj = datetime.strptime(last_read, '%Y-%m-%d %H:%M:%S')
        formatted_date = date_time_obj.strftime("%d %B, %Y %H:%M %p")
    else:
        formatted_date = None
    if len_data > 0:
        for row in result:
            alarm_dict = {}
            alarm_dict["source_ip"] = row[0]
            alarm_dict["destination_ip"] = row[1]
            alarm_dict["plugin_sid"] = row[2]
            alarm_dict["risk"] = row[3]
            alarm_dict["timestamp"] = row[4]
            alarm_dict["name"] = row[5]
            data.append(alarm_dict)
        json_dict["last_read"] = formatted_date
        json_dict["count"] = len_data
        json_dict["data"] = data
    else:
        json_dict["last_read"] = formatted_date
        json_dict["count"] = 0
        json_dict["data"] = []
    json_obj = json.dumps(json_dict)
    json_obj = json.loads(json_obj)
    tmp.close()
    cursor.close()
    conn.close()
    return jsonify(json_obj)
