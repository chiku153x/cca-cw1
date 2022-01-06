import boto3
import botocore
import json
import os


s3 = boto3.resource('s3')

BUCKET = os.environ['BUCKET']
OUTPREFIX = os.environ['OUTPREFIX']



def csv2sql(csv,sql):
    with open(csv) as f:
        lines = f.readlines()
    if len(lines) > 0 :
        count = 0
        rows = ""
        for line in lines:
            count = count + 1
            if count > 1:
                va = line.split(',')
                rows = rows + "INSERT INTO users (ID,NAME,AGE,GENDER) values ({0},'{1}','{2}','{3}');".format(va[0],va[1],va[2],va[3]) + "\n"
        with open(sql, 'w') as f:
            f.write(rows)    
    else:
        print("No data in the csv")   


def lambda_handler(event, context):
    print(json.dumps(event))
    key = event['Records'][0]['s3']['object']['key']
    filename= key.split('/')[-1]
    csvpath = "/tmp/" + filename
    sqlpath = "/tmp/" + filename.replace('csv','sql')
    try:
        s3.Bucket(BUCKET).download_file(key, csvpath)
        csv2sql(csvpath,sqlpath)
        s3.Bucket(BUCKET).upload_file(sqlpath, OUTPREFIX + "/" + filename.replace('csv','sql'))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("Object does not exist")
        else:
            raise

