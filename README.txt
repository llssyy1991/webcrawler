###All code here are written by ourselves.

###Copty right by Shouwei and Siyuan.

Our found contain several parts as follows:

1)Crawler to get information from website:

1)install python selenium first:
http://selenium-python.readthedocs.org/installation.html

2)install mongodb
https://www.mongodb.org/downloads#production

3install pymongo
https://api.mongodb.org/python/current/

4)Firefox
https://www.mozilla.org/en-US/firefox/new/?product=firefox-3.6.8&os=osx%E2%8C%A9=en-US

5) createhashdatacollection db.createCollection(“hashdata”)
After install these tools, you can run your crawler on your computer.

There’s a few things you should know:
1) Using Google too much will be blocked for a while by google.
2) Before you run your code, you must keep your mongodb availiable.
3) During program running, web browser will be create, don’t shut it down.

2)python file to filter out repeated information is also include in first crawler part.

2)scala file to analyze company detection rate:
After you configure spark-hadoop2.6 version and modify the path in this file, you can just run this scala file.
We provide the simplified data set for this program.

4)scala file to find corresponding information in database:
After you configure spark-hadoop2.6 version and modify the path in this file, you can just run this scala file.
We provide the simplified data set for this program.