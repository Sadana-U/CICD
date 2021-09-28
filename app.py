from flask import Flask , render_template , redirect ,request
import json
import requests
import numpy as np
import urllib.request
from PIL import Image
from datetime import datetime, timedelta
from azure.storage.blob import ContainerClient,ContentSettings
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from azure.storage.blob import BlobClient,BlobServiceClient


account_name = "sadana5498021157"
account_key = "yJ72oyGq7KNVHB/EC0RHZLWofdrKZ50Q5Ra+BAt2aHrXU3OOOAUy7fDhN7zy27HV2KIAcZbnkHtz0yWxdsGThA=="
container_name = "images"
container = ContainerClient.from_connection_string(conn_str="BlobEndpoint=https://sadana5498021157.blob.core.windows.net/;QueueEndpoint=https://sadana5498021157.queue.core.windows.net/;FileEndpoint=https://sadana5498021157.file.core.windows.net/;TableEndpoint=https://sadana5498021157.table.core.windows.net/;SharedAccessSignature=sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacuptfx&se=2021-09-30T12:13:45Z&st=2021-09-15T04:13:45Z&spr=https&sig=%2FR61cSPsa4lZUT%2BE6gzd0cZ%2FmpDgRYaRwKguDXXg4XA%3D", container_name=container_name)
container_SASconnection_string="DefaultEndpointsProtocol=https;AccountName=sadana5498021157;AccountKey=yJ72oyGq7KNVHB/EC0RHZLWofdrKZ50Q5Ra+BAt2aHrXU3OOOAUy7fDhN7zy27HV2KIAcZbnkHtz0yWxdsGThA==;EndpointSuffix=core.windows.net"
app = Flask(__name__)



@app.route('/')
def index():
    return render_template("home.html")

@app.route('/data',methods=[ 'POST' ])


def login():

    if request.method=='POST':
        uploaded = request.files['data']
        filename=secure_filename(uploaded.filename)
        print(filename)
        blob = BlobClient.from_connection_string("BlobEndpoint=https://sadana5498021157.blob.core.windows.net/;QueueEndpoint=https://sadana5498021157.queue.core.windows.net/;FileEndpoint=https://sadana5498021157.file.core.windows.net/;TableEndpoint=https://sadana5498021157.table.core.windows.net/;SharedAccessSignature=sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacuptfx&se=2021-09-30T12:13:45Z&st=2021-09-15T04:13:45Z&spr=https&sig=%2FR61cSPsa4lZUT%2BE6gzd0cZ%2FmpDgRYaRwKguDXXg4XA%3D", container_name=container_name, blob_name=filename)
        blob.upload_blob(uploaded)

        blob_list = container.list_blobs()
        for blob in blob_list:
            hey=blob.name
            print(hey + '\n')


        var1="https://sadana5498021157.blob.core.windows.net/images/"
        urlget=var1+hey
        data = Image.open(requests.get(urlget, stream=True).raw)
        print(data)
        print(type(data))
        data=data.resize((28,28))
        Image_array=np.array(data)
        normalised_data=Image_array/255.0
        re_shape=normalised_data.reshape(1,-1)
        list_data=re_shape.tolist()
        print(normalised_data.shape)
        print("***************")
        print(normalised_data)
        print(list_data)

        json_input=json.dumps({"data":list_data})


        print(data)
        print(type(data))

        
        url = 'http://f50edca4-c772-43a1-82d2-c4df15b418c0.eastus.azurecontainer.io/score'
        headers = {'Content-Type':'application/json'}
        r = requests.post(url,json_input,headers=headers)
        res=r.text
        print(res)

        blob_list = container.list_blobs()
        for blob in blob_list:
            hey=blob.name
            container.delete_blob(hey)

        return render_template("resp.html", res=res)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)

 