# import the library
from appJar import gui

import pyodbc
import jaydebeapi
import jpype

import time


#CONNESSIONE A DB2
jar = 'db2as400.jar' # location of the jdbc driver jar
args='-Djava.class.path=%s' % jar
jvm = jpype.getDefaultJVMPath()
jpype.startJVM(jvm, args)
conn=jaydebeapi.connect('com.ibm.as400.access.AS400JDBCDriver', 'jdbc:as400://10.1.12.180:50000',['QSECOFR','tony34']) #connessione al db2
curs=conn.cursor()
#########FINE DB2

curs.execute("SELECT * FROM CATERINA.VET_TRASP")
righe = curs.fetchall()
for riga in righe:
	print(riga)


