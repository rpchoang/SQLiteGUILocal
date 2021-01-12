import sqlite3
from sqlite3 import Error
import csv


def dataload(filename):

	with open(filename, 'r') as f:
		reader = csv.reader(f)
		datalist = list(reader)

	dataarray = []

	for i in datalist:
		name = i[0]
		yieldstr = i[1]
		ultstr = i[2]
		elong = i[3]

		if '-' in yieldstr:
			yieldstrl = yieldstr[0:yieldstr.index('-')-2]
			yieldstrh = yieldstr[yieldstr.index('-') + 3:len(yieldstr)]
		else:
			yieldstrl = yieldstr
			yieldstrh = yieldstr

		if '-' in ultstr:
			ultstrl = ultstr[0:ultstr.index('-')-2]
			ultstrh = ultstr[ultstr.index('-') + 3:len(ultstr)]
		else:
			ultstrl = ultstr
			ultstrh = ultstr

		if '-' in elong:
			elongl = elong[0:elong.index('-')-2]
			elongh = elong[elong.index('-') + 3:len(elong)]
		else:
			elongl = elong
			elongh = elong

		payload = [name, yieldstrl, yieldstrh, ultstrl, ultstrh, elongl, elongh]
		dataarray.append(payload)

	return dataarray


def databaseconnect(dbfile):
	conn = None
	try:
		conn = sqlite3.connect(dbfile)
		print(sqlite3.version)
		return conn
	except Error as e:
		print(e)
	

	return conn


def createtable(conn, create_table_sql):
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)


def createmechprop(conn, mechprop):
	sql = ''' INSERT INTO metalmechproperties(name, yieldstrlo, yieldstrhi, ulttensilestrlo, ulttensilestrhi, elongationlo, elongationhi, hardnesslo, hardnesshi, thermcoefflo, thermcoeffhi)
				VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
	c = conn.cursor()
	c.execute(sql, mechprop)
	conn.commit()
	return c.lastrowid


def createchemprop(conn, connprop):
	sql = ''' INSERT INTO metalchemproperties(name, si, fe, cu, mn, mg, zn, ti, sn, ni, al)
				VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
	c = conn.cursor()
	c.execute(sql,connprop)
	conn.commit()
	return c.lastrowid


def main():
	dataarray = dataload("pg1yieldultimateelong.csv")
	for i in dataarray:
		print(i)

	conn = databaseconnect(r"materials.db")

	metals_mech_properties = """ CREATE TABLE IF NOT EXISTS metalmechproperties (
									id integer PRIMARY KEY,
									name text NOT NULL,
									yieldstrlo integer,
									yieldstrhi integer,
									ulttensilestrlo integer,
									ulttensilestrhi integer,
									elongationlo real,
									elongationhi real,
									hardnesslo real,
									hardnesshi real,
									thermcoefflo real,
									thermcoeffhi real
								); """


	metals_chem_properties = """ CREATE TABLE IF NOT EXISTS metalchemproperties (
									id integer PRIMARY KEY,
									name text NOT NULL,
									si real,
									fe real,
									cu real,
									mn real,
									mg real,
									zn real,
									ti real,
									sn real,
									ni real,
									al real,
									FOREIGN KEY (name) REFERENCES metalmechproperties (name)
								); """

	if conn is not None:
		createtable(conn, metals_mech_properties)
		createtable(conn, metals_chem_properties)
		for i in dataarray:
			mechprop = (i[0], i[1], i[2], i[3], i[4], i[5], i[6], 0, 0, 0, 0)
			idnum = createmechprop(conn, mechprop)
	else:
		print("Error! connot create database connection!")


if __name__ == "__main__":
	main()