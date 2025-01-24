import boto3
import json
import datetime
import os
import urllib.request
_env = os.environ

#メイン処理
def lambda_handler(event, context):
    #請求情報取得
    _billing = getBillingMetric()
    _billing["message"] = "現時点のAWS請求金額は $" + str(_billing['Datapoints'][0]['Maximum']) + " です。"
    #LINEに送信
    sendNoticeToLine(_billing)

def getBillingMetric():
    _cw = boto3.client('cloudwatch', region_name=_env["REGION"])
    _billing = _cw.get_metric_statistics(
        Namespace='AWS/Billing',
        MetricName='EstimatedCharges',
        Dimensions=[{'Name': 'Currency', 'Value': 'USD'}],
        StartTime=datetime.datetime.today() - datetime.timedelta(days=1),
        EndTime=datetime.datetime.today(),
        Period=86400,
        Statistics=['Maximum'])

    print(_billing)
    return _billing

def sendNoticeToLine(_bill):
    _url = 'https://notify-api.line.me/api/notify'
    _data = {
      "message": _bill["message"]
    }
    _header = {
      "Authorization": "Bearer " + _env["LINE_ACCESS_TOKEN"]
    }

    print(_data)
    sendRequest(_url, _data, _header)

def sendRequest(_url, _data, _header):
    _data = urllib.parse.urlencode(_data).encode("utf-8")
    _req = urllib.request.Request(_url, _data, _header, "POST")
    try:
        with urllib.request.urlopen(_req) as _res:
            _body = _res.read()
            print(_body)
    except urllib.error.HTTPError as _err:
        print("HTTPError: " + str(_err.code))
        print(_err)
    except urllib.error.URLError as _err:
        print("HTTPError: " + _err.reason)
        print(_err)
