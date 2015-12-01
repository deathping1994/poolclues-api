from elasticsearch import Elasticsearch
import re

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
csvfile=open("/home/gaurav/Affiliate_feed.csv","r")
fields=csvfile.readline()
fields=fields.split(",")
jsonobj={}
i=0
for line in csvfile:
    line = re.sub('[\"]','',line)
    line=line.split(",")
    if len(line)>=26:
        jsonobj["Product ID"]=line[0]
        jsonobj["Product URL"]=line[1]
        jsonobj["Product Name"]=line[2]
        jsonobj["Category Id"]=line[3]
        jsonobj["MRP"]=line[4]
        jsonobj["Discount (percentage)"]=line[5]
        jsonobj["image_path"]=line[6]
        jsonobj["Meta category"]=line[7]
        jsonobj["Price"]=line[8]
        jsonobj["Brand"]=line[9]
        jsonobj["COD"]=line[10]
        jsonobj["Shipping Cost"]=line[11]
        jsonobj["EMI"]=line[12]
        jsonobj["Stock"]=line[13]
        jsonobj["Deal"]=line[14]
        jsonobj["FreeBee Inside"]=line[15]
        jsonobj["Category Path"]=line[16]
        jsonobj["Customer_type"]=line[17]
        jsonobj["Gender"]=line[18]
        jsonobj["Leaf CategoryId"]=line[19]
        jsonobj["Leaf Category"]=line[20]
        jsonobj["Warranty"]=line[21]
        jsonobj["Product Label1"]=line[22]
        jsonobj["Product Label2"]=line[23]
        jsonobj["Product Label3"]=line[24]
        jsonobj["Product Label4"]=line[25]
        print jsonobj
        try:
            es.index(index='products',id=line[0],doc_type='product', body=jsonobj)
        except IndexError as err:
            pass
        except Exception as e:
            pass
        continue

__author__ = 'gaurav'
