import requests
import json


ENV = {'Prod': 'Prod'}
GET_SIGNED_URL_LAMBDA = "https://x85g09c3v6.execute-api.eu-west-1.amazonaws.com/" + ENV['Prod'] + "/getsigned"

OBJ_NAME = 'data_new_file.csv'


data = {'file_name': OBJ_NAME}
headers = {'x-api-key': 'Oxl93RegPB6q85DhxtshG8juTc106xcP9gV7TF3c'}
r = requests.post(GET_SIGNED_URL_LAMBDA, json=data, headers=headers)
print(r.status_code)
if r.status_code == 200:
	j = json.loads(r.content)
	print(json.dumps(j))

	# upload file via presigned url
	files = {'file': open(OBJ_NAME, 'rb')}
	x = requests.post(j['url'], data=j['fields'], files=files)
	print(x.status_code)

	if x.status_code ==204:
		print(OBJ_NAME + " is uploaded to s3")
	else:
		print('File did not upload')
else:
	print("Could not get signed url")
