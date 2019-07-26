import requests
import json
import time

headers = {
'Accept-Encoding': 'gzip',
"User-Agent":"Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1",
'Connection':'keep-alive',
'Host': 'aweme.snssdk.com',
'X-SS-REQ-TICKET': '1536115411835'}

cookies = {'install_id': '43077011048', 'odin_tt': 'f024c8496af17ad75cb9ea83e394172ecfd9d666f3731ad98e0379e4d1759a647c011ac8fe2ad16341af8fb2d8d50d5b', 'sessionid': '2ea5ae2cedc3e21cfb0505c81cf274a8', 'sid_guard': '2ea5ae2cedc3e21cfb0505c81cf274a8%7C1535966164%7C5184000%7CFri%2C+02-Nov-2018+09%3A16%3A04+GMT', 'sid_tt': '2ea5ae2cedc3e21cfb0505c81cf274a8', 'ttreq': '1$3ec8eb5df7a83e7dd1969afeee7784dc0be0438b', 'uid_tt': 'cc6e039997a7c451b4123bbfafaad805'}
url = 'https://aweme.snssdk.com/aweme/v1/discover/search/?iid=43077011048&device_id=36894652689&os_api=18&app_name=aweme&channel=App%20Store&idfa=9E4F6E17-0A00-4F85-8630-CB9CECC6B52B&device_platform=iphone&build_number=25105&vid=BBCCF487-80AA-4177-8CC0-5C12ABCC8FC0&openudid=1e85eb9f4463291a2c3f90be6a0d43be92b8cf58&device_type=iPhone7,2&app_version=2.5.1&version_code=2.5.1&os_version=11.4.1&screen_width=750&aid=1128&ac=WIFI&count=20&cursor=0&keyword=%E5%A4%96%E6%B1%87&search_source=discover&type=1&mas=010d3956dac0aaa5b85f9b628e908d651ee74c4a07b87ffc822eb8'
response = requests.get(url=url,headers=headers,cookies=cookies)
print(json.loads(response.content))



