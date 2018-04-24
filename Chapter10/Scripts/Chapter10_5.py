import pyarrow as pa
import pandas as pd
from pymapd import connect
import shapefile
connection = connect(user="mapd", password= "i-dfsfsdfsdfwq", 
     host="ec2-34-78-82.us-west-2.compute.amazonaws.com", dbname="mapd")
cursor = connection.cursor()


create = """CREATE TABLE juneau_addresses (  
	LON FLOAT, LAT FLOAT, 
	SNUMBER VARCHAR(30),STREET VARCHAR(200) );
"""

cursor.execute(create)
df = pd.read_csv('city_of_juneau.csv')
table = pa.Table.from_pandas(df)
print(table)
connection.load_table("juneau_addresses", table)


cursor.execute(create)
df = pd.read_csv('calaveras.csv')
table = pa.Table.from_pandas(df)
print(table)
connection.load_table_rowwise("addressescalaveras", df)
