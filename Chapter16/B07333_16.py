from pywebhdfs.webhdfs import PyWebHdfsClient as h 
hdfs=h(host='sandbox.hortonworks.com',port='50070',user_name='raj_ops')


ls=hdfs.list_dir('/')


ls['FileStatuses']['FileStatus'][0] 


hdfs.make_dir('/samples',permission=755) 
f=open('/home/pcrickard/sample.csv') 
d=f.read() 
hdfs.create_file('/samples/sample.csv',d) 


hdfs.read_file('/samples/sample.csv') 


hdfs.get_file_dir_status('/samples/sample.csv') 


from pyhive import hive 
c=hive.connect('sandbox.hortonworks.com').cursor() 
c.execute('CREATE TABLE FromPython (age int, name string)  ROW FORMAT DELIMITED FIELDS TERMINATED BY ","')  

c.execute("LOAD DATA INPATH '/samples/sample.csv' OVERWRITE INTO TABLE FromPython")
c.execute("SELECT * FROM FromPython") 
result=c.fetchall() 

