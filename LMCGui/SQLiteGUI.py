from tkinter import *
from PIL import ImageTk,ImageTk
from tkinter import PhotoImage
from tkinter import ttk
import sqlite3
import os
import multiprocessing
multiprocessing.set_start_method('spawn')

from multiprocessing.managers import BaseManager


"""
 @ORIGINAL AUTHOR - RONALD HOANG 1/6/2021

 This program gives us an easy to use GUI to explore a Lordstown Motor's material database and its mechanical properties
 Python Program to edit, search, add, and delete from this database, we look at yield str, ultimate tensile str, elongation at yield, hardness, and CTE
 Datbase is based off of SQLite3
 GUI is written in tkinter

 ------FEATURES V1.0.1--------
 Add materials to database, if empty then will leave the corresponding area in the database blank, still able to edit later
 Search database based on any of the mechanical properties or a combination of any of the properties 
 		Search based on input being in range, or known material property being within bounds we list
 		Set the MIN MAX values of the property, or have the input listed be checked to be in the min max values of the material
 		Leave inputs blank to search 
 		Opens a seperate window for you to explore your search results
 		Refresh button for Search results to see yourself edit, add, or remove entries into the database
 Edit or Delete an entry based on known ID #
 		New window pops up when button is pressed 
 		Can update individual values or many at once for a single database entry
 		Commit changes and click refresh button on the search window to see the value be updated
 		Delete buggy when not deleting the last entry # when clicking refresh on the search window but database does update just exit search and do it again to see proper changes

 TODO
 - Add more mechanical properties: Density, Thermal Conductivity, Electrical Conductivity, Melting Point, Youngs Modulus, Specific Heat Capacity
 - Implement features to search for either chemical properties/composition or mechanical properties or both
 - Implement a better "close enough" name search
 - Plan to have a less memory intensive way of looking at all entries without having to list them all at once
 - Have a main menu rather than a mish mash of stuff together
 - Find more data to add to database
 - Implement Entry box sanity checkers to ensure only correct input is passed through
 - Make an executable
 - Bug fix refresh button, deleting/adding an entry will sometimes make it so the scrolling window doesn't resize properly but does update the actual database still


"""
databaseroute = os.path.join(os.path.expanduser("~"),"Lordstown Motors Corp", "Battery & Propulsion Team - General","Documents", "materials.db")
root = Tk()
root.title('Lordstown Motors Materials Database')
root.geometry("900x650")
root.iconbitmap('Lordstown.ico')
root["bg"] = "#42414A"

entryedits = []


def labelformat(labels):
	for i in labels:
		i.configure(bg = "#42414A", fg = "white")

def entryformat(entries):
	for i in entries:
		i.configure(bg = "#a0a0a4")

def buttonformat(buttons):
	for i in buttons:
		i.configure(bg = "#a0a0a4", fg = "white")

def checkformat(checks):
	for i in mychecks:
		i.configure(bg = "#42414A", fg = "white", selectcolor = "#42414A", activebackground = "#42414A", activeforeground = "white")

def clearentries(entries):
	for i in entries:
		i.delete(0,END)


def submit():
	conn = sqlite3.connect(databaseroute)
	c = conn.cursor()
	sql = ("INSERT INTO metalmechproperties(name, yieldstrlo, yieldstrhi, ulttensilestrlo, ulttensilestrhi, hardnesslo, hardnesshi, elongationlo, elongationhi, thermcoefflo, thermcoeffhi) VALUES (?,?,?,?,?,?,?,?,?,?,?)")
	mechprop = (name.get(), yieldstrlo.get(), yieldstrhi.get(), ulttensilstrlo.get(), ulttensilstrhi.get(), hardnesslo.get(), hardnesshi.get(), elongationlo.get(), elongationhi.get(), thermcoefflo.get(), thermcoeffhi.get())
	c.execute(sql,mechprop)
	conn.commit()
	clearentries(myentries)


def isempty(inputs):
	output = False
	for i in inputs:
		if len(i.get()) != 0:
			output = True

	return output



def displaysearch(c,sql):
	c.execute(sql)
	rows = c.fetchall()

	#for r in rows:
	#	print(r)

	wind = Toplevel(root)
	wind.title('Lordstown Motors Materials Database Search Results')
	wind.geometry("1000x570")
	wind.iconbitmap("Lordstown.ico")
	wind["bg"] = "#42414A"
	wind.grid_columnconfigure(0, weight = 1)

	intro = Label(wind, text = "\nSEARCH RESULTS:", fg = "white", bg = "#42414A")
	intro.grid(row = 0, column = 0,sticky = "ew")

	frame_canvas = Frame(wind)
	frame_canvas.grid(row=1, column=0, pady = 10, sticky = "news")
	frame_canvas.grid_columnconfigure(0, weight=1)
	frame_canvas.grid_rowconfigure(0, weight=1)
	canvas = Canvas(frame_canvas, bg="white")
	canvas.grid(row=0, column=0, ipady = 80, sticky="news")

	vsb = Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
	vsb.grid(row=0, column=1, sticky='nws')
	canvas.configure(yscrollcommand=vsb.set)
	hsb = Scrollbar(frame_canvas, orient="horizontal", command=canvas.xview)
	hsb.grid(row=1, column=0, sticky='sew')
	canvas.configure(xscrollcommand=vsb.set)

	table = Frame(canvas)
	table.grid_columnconfigure(0, weight = 1)
	canvas.create_window((0, 0), window=table)
	resultstable = [[Label() for i in range (len(rows[0]))] for i in range(len(rows)) ]

	iDtableLabel = Label(table, text = "ID #")
	iDtableLabel.grid(row = 0, column = 0)

	nametableLabel = Label(table, text = "Material Name")
	nametableLabel.grid(row = 0, column = 1)

	yieldstrlabel = Label(table, text = "Yield Strength\n Range (MPa)")
	yieldstrlabel.grid(row = 0, column = 2, columnspan = 2)

	ulttenslabel = Label(table, text = "Ultimate Tensile Strength\n Range (MPa)")
	ulttenslabel.grid(row = 0, column = 4, columnspan = 2)

	elonglabel = Label(table, text = "Elongation at Yield\n Range (%)")
	elonglabel.grid(row = 0, column = 6, columnspan = 2)

	hardnesslabel = Label(table, text = "Hardness\n Range (HB)")
	hardnesslabel.grid(row = 0, column = 8, columnspan = 2)

	thermlabel = Label(table, text = "Coefficient of Thermal\nExpansion Range (um/mC)")
	thermlabel.grid(row = 0, column = 10, columnspan = 2)

	for r in range(len(rows)):
		for x in range(len(rows[r])):
			resultstable[r][x] = Label(table, text=(rows[r][x]))
			resultstable[r][x].grid(row = r+1, column = x, sticky = "ew")

			if x%2 == 0:
				resultstable[r][x].configure(bg = "#d3d3d3")

	numrows = len(rows)
	numcols = len(rows[0])
#	for i in range(numcols):
#		ttk.Separator(table, orient = "vertical").grid(column = i, row = 1, rowspan = numrows + 1, sticky = 'nse')

	for i in range(numrows):
		ttk.Separator(table, orient = "horizontal").grid(column = 0, row = i, columnspan = numcols+1, sticky = "sew")

	refresh = Button(wind, text = "Refresh Page", command = lambda: reloadtable(resultstable, rows, sql, table, canvas))
	refresh.grid(row = 2, column = 0, ipadx = 5, pady = 10)
	buttonrefresh = [refresh]
	buttonformat(buttonrefresh)
	table.update_idletasks();



	canvas.config(scrollregion=canvas.bbox("all"))


def reloadtable(resultstable, rows, sql, table, canvas):

	for r in range(len(rows)):
		for x in range(len(rows[r])):
			resultstable[r][x].destroy()

	table.update_idletasks()
	canvas.update()

	conn = sqlite3.connect(databaseroute)
	c = conn.cursor()
	c.execute(sql)
	rows = c.fetchall()
	numrows = len(rows)
	numcols = len(rows[0])
	resultstable2 = [[Label() for i in range (len(rows[0]))] for i in range(len(rows)) ]


	for r in range(len(rows)):
		for x in range(len(rows[r])):
			resultstable2[r][x]=Label(table, text=(rows[r][x]))
			resultstable2[r][x].grid(row = r+1, column = x, sticky = "ew")
			if x%2 == 0:
				resultstable2[r][x].configure(bg = "#d3d3d3")

	for i in range(numrows):
		ttk.Separator(table, orient = "horizontal").grid(column = 0, row = i, columnspan = numcols+1, sticky = "sew")


	table.update_idletasks();

	canvas.config(scrollregion=canvas.bbox("all"))




def wherestatement():
	out = " WHERE "
	first = True

	if len(minyield.get()) != 0:
		if minvaryield.get():
			out += "yieldstrlo >= {} ".format(minyield.get())
			first = False
		else:
			out += "{} BETWEEN yieldstrlo AND yieldstrhi ".format(minyield.get())
			first = False

	if len(maxyield.get()) != 0:
		if not first:
			out += "AND "
		if maxvaryield.get():
			out += "yieldstrhi <= {} ".format(maxyield.get())
			first = False

	if len(minult.get()) != 0:
		if not first:
			out += "AND "
		if minvarult.get():
			out += "ulttensilestrlo >= {} ".format(minult.get())
			first = False
		else:
			out += "{} BETWEEN ulttensilestrlo AND ulttensilestrhi ".format(minult.get())
			first = False

	if len(maxult.get()) != 0:
		if not first:
			out += "AND "
		if maxvarult.get():
			out += "ulttensilestrhi <= {} ".format(maxult.get())
			first = False

	if len(minelo.get()) != 0:
		if not first:
			out += "AND "
		if minvarelo.get():
			out += "elongationlo >= {} ".format(minelo.get())
			first = False
		else:
			out += "{} BETWEEN elongationlo AND elongationhi ".format(minelo.get())
			first = False

	if len(maxelo.get()) != 0:
		if not first:
			out += "AND "
		if maxvarult.get():
			out += "elongationhi <= {} ".format(maxelo.get())
			first = False


	if len(minhard.get()) != 0:
		if not first:
			out += "AND "
		if minvarhard.get():
			out += "hardnesslo >= {} ".format(minhard.get())
			first = False
		else:
			out += "{} BETWEEN hardnesslo AND hardnesshi ".format(minelo.get())
			first = False

	if len(maxhard.get()) != 0:
		if not first:
			out += "AND "
		if maxvarhard.get():
			out += "hardnesshi <= {} ".format(maxhard.get())
			first = False


	if len(mintherm.get()) != 0:
		if not first:
			out += "AND "
		if minvartherm.get():
			out += "thermcoefflo >= {} ".format(mintherm.get())
			first = False
		else:
			out += "{} BETWEEN thermcoefflo AND thermcoeffhi ".format(mintherm.get())
			first = False

	if len(maxtherm.get()) != 0:
		if not first:
			out += "AND "
		if maxvartherm.get():
			out += "thermcoeffhi <= {} ".format(maxtherm.get())
			first = False

	if len(nameval.get()) != 0:
		if not first:
			out +="AND "
		out += "name LIKE '%{}%' ".format(nameval.get())


	return out

def search():
	conn = sqlite3.connect(databaseroute)
	c = conn.cursor()
	sql = ("SELECT * FROM metalmechproperties")
	if not isempty(myentries):
		sql += ";"
		displaysearch(c,sql)
	else: 
		sql += wherestatement()
		displaysearch(c,sql)


def edit():

	wind = Toplevel(root)
	wind.title('Lordstown Motors Materials Database Editor')
	wind.geometry("450x400")
	wind.iconbitmap("Lordstown.ico")
	wind["bg"] = "#42414A"


	edittitle = Label(wind, text= "\nEDIT A MATERIAL ENTRY \n Please input the ID# of the material you'd like to edit or delete \n Fill out the relevant fields you'd like to change leave blank to leave field unedited\n", bg = "#42414A", fg = "white")
	edittitle.grid(row = 0, column = 0, sticky = "ew")

	editframe = Frame(wind)
	editframe.grid(row = 1, column = 0)
	editframe["bg"] = "#42414A"

	idNumber = Label(editframe, text="ID#")
	idNumber.grid(row=0, column = 0,sticky = "ne")

	identry = Entry(editframe, width = 10)
	identry.grid(row=0, column = 1, padx = 5, sticky = "nw")

	nameedit = Label(editframe, text=" Name\n")
	nameedit.grid(row = 0, column =2, sticky = "ne")

	nameentry = Entry(editframe, width = 20)
	nameentry.grid(row = 0, column = 3, padx = 5, sticky = "nw")

	editentries = Frame(editframe)
	editentries.grid(row = 1, column = 0, columnspan = 4)
	editentries["bg"] = "#42414A"



	rangelabel = Label(editentries, text = "Range")
	rangelabel.grid(row = 0, column = 0, padx = 10)

	minlabel = Label(editentries, text = "Min")
	minlabel.grid(row = 0, column = 1)

	maxlabel = Label(editentries, text = "Max")
	maxlabel.grid(row = 0, column = 2)

	yieldlabel = Label(editentries, text = "Yield Strength (MPa)")
	yieldlabel.grid(row=1,column = 0,padx = 10)

	ultlabel = Label(editentries, text = "Ultimate Tensile Strength (MPa)")
	ultlabel.grid(row=2, column = 0,padx = 10)

	elolabel = Label(editentries, text = "Elongation at Yield (%)")
	elolabel.grid(row = 3, column = 0, padx = 10)

	hardlabel = Label(editentries, text = "Hardness (HB)")
	hardlabel.grid(row = 4, column = 0, padx = 10)

	ctelabel = Label(editentries, text = "Coefficient of Thermal\nExpansion (um/mC)")
	ctelabel.grid(row=5, column = 0, padx = 10)

	editlabels = [edittitle, idNumber, nameedit, rangelabel, minlabel, maxlabel, yieldlabel, ultlabel, elolabel, hardlabel, ctelabel]
	labelformat(editlabels)

	yieldmin = Entry(editentries, width = 15)
	yieldmin.grid(row = 1, column = 1, padx = 10, pady = 2)

	yieldmax = Entry(editentries, width = 15)
	yieldmax.grid(row = 1, column = 2, padx = 10, pady = 2)

	tensmin = Entry(editentries, width = 15)
	tensmin.grid(row = 2, column = 1, padx = 10 ,pady = 2)

	tensmax = Entry(editentries, width = 15)
	tensmax.grid(row = 2, column = 2, padx = 10, pady = 2)

	elomin = Entry(editentries, width = 15)
	elomin.grid(row = 3, column = 1, padx = 10, pady = 2)

	elomax = Entry(editentries, width = 15)
	elomax.grid(row = 3, column =2 , padx = 10, pady = 2)

	hardmin = Entry(editentries, width = 15)
	hardmin.grid(row = 4, column = 1, padx = 10, pady = 2 )

	hardmax = Entry(editentries, width = 15)
	hardmax.grid(row = 4, column = 2, padx = 10, pady = 2)

	ctemin = Entry(editentries, width = 15)
	ctemin.grid(row = 5, column = 1, padx = 10, pady =2, sticky = "n")

	ctemax = Entry(editentries, width = 15)
	ctemax.grid(row = 5, column = 2, padx = 10, pady = 2 , sticky = "n")

	entryedits = [identry, nameentry, yieldmin, yieldmax, tensmin, tensmax, elomin, elomax, hardmin, hardmax, ctemin, ctemax]
	entryformat(entryedits)

	commitchanges = Button(wind, text = "Commit Changes", command = lambda: editentry(entryedits))
	commitchanges.grid(row = 2, column = 0, ipadx = 100, pady = 10)

	deleteentry = Button(wind, text = "Delete Entry", command = lambda: [removeentry(identry.get()),clearentries(entryedits)])
	deleteentry.grid(row = 3, column = 0, ipadx = 115, pady = 10)

	editbuttons = [commitchanges, deleteentry]
	buttonformat(editbuttons)

def removeentry(idval):
	sql = ("DELETE FROM metalmechproperties WHERE id = {}".format(idval))
	conn =sqlite3.connect(databaseroute)
	curr = conn.cursor()
	curr.execute(sql)
	conn.commit()	

def setvalues(mechpropset):
	output = ""
	first = True
	if len(mechpropset[1].get()) != 0:
		output += (" name = '{}'").format(mechpropset[1].get())
		first = False

	if len(mechpropset[2].get()) != 0:
		if not first:
			output += ","
		output += (" yieldstrlo = '{}'".format(mechpropset[2].get()))
		first = False

	if len(mechpropset[3].get()) != 0:
		if not first:
			output+= ","
		output += (" yieldstrhi = '{}'".format(mechpropset[3].get()))
		first = False

	if len(mechpropset[4].get()) != 0:
		if not first:
			output+= ","
		output += (" ulttensilestrlo = '{}'".format(mechpropset[4].get()))
		first = False

	if len(mechpropset[5].get()) != 0:
		if not first:
			output += ","
		output += (" ulttensilestrhi = '{}'".format(mechpropset[5].get()))
		first = False

	if len(mechpropset[6].get()) != 0:
		if not first:
			output += ","
		output += (" elongationlo = '{}'".format(mechpropset[6].get()))
		first = False

	if len(mechpropset[7].get()) != 0:
		if not first:
			output += ","
		output += (" elongationhi = '{}'".format(mechpropset[7].get()))
		first = False

	if len(mechpropset[8].get()) != 0:
		if not first: 
			output += ","
		output += (" hardnesslo = '{}'".format(mechpropset[8].get()))
		first = False

	if len(mechpropset[9].get()) != 0:
		if not first:
			output += ","
		output += (" hardnesshi = '{}'".format(mechpropset[9].get()))
		first = False


	if len(mechpropset[10].get()) != 0:
		if not first:
			output += ","
		output += (" thermcoefflo = '{}'".format(mechpropset[10].get()))
		first = False

	if len(mechpropset[11].get()) != 0:
		if not first:
			output += ","
		output += (" thermcoeffhi = '{}'".format(mechpropset[11].get()))
		first = False

	return output




def editentry(entryedits):
	sql = ("UPDATE metalmechproperties SET")
	sql += setvalues(entryedits)
	sql += ("WHERE id = {}".format(entryedits[0].get()))

	conn = sqlite3.connect(databaseroute)
	curr = conn.cursor()
	curr.execute(sql)
	conn.commit()
	clearentries(entryedits)



'''----------------------------------------------------------------------------------------------------------'''


name = Entry(root, width=20)
name.grid(row=1,column=1,padx=10)

yieldstrlo = Entry(root, width=20)
yieldstrlo.grid(row=2,column=1)

yieldstrhi = Entry(root, width=20)
yieldstrhi.grid(row=2,column=3)

ulttensilstrlo = Entry(root, width=20)
ulttensilstrlo.grid(row=3,column=1)

ulttensilstrhi = Entry(root, width=20)
ulttensilstrhi.grid(row=3,column=3)

elongationlo = Entry(root, width=20)
elongationlo.grid(row=4,column=1)

elongationhi = Entry(root, width=20)
elongationhi.grid(row=4,column=3)

hardnesslo = Entry(root, width=20)
hardnesslo.grid(row=5,column=1)

hardnesshi = Entry(root, width=20)
hardnesshi.grid(row=5,column=3)

thermcoefflo = Entry(root, width=20)
thermcoefflo.grid(row=6,column=1)

thermcoeffhi = Entry(root, width=20)
thermcoeffhi.grid(row=6,column=3)


additiontitle = Label(root, text = "\nADD MATERIAL TO DATABASE:\nPlease search for the name of the metal before adding and see if values need to be edited")
additiontitle.grid(row=0, column = 0, columnspan = 4)

namelabel = Label(root, text = "Name")
namelabel.grid(row=1,column=0)


yieldlolabel = Label(root, text = "Lower Yield Strength (MPa)")
yieldlolabel.grid(row=2,column=0)

yieldhilabel = Label(root, text = "Higher Yield Strength (MPa)")
yieldhilabel.grid(row=2,column=2)

tenslolabel = Label(root, text = "Lower Ultimate Tensile Strength (MPa)")
tenslolabel.grid(row=3,column=0)

tenshilabel = Label(root, text = "Higher Ultimate Tensile Strength (MPa)")
tenshilabel.grid(row=3,column=2)

elonglolabel = Label(root, text = "Lower Elongation at Yield (%)")
elonglolabel.grid(row=4,column=0)

elonghilabel = Label(root, text = "Higher Elongation at Yield (%)")
elonghilabel.grid(row=4,column=2)

hardlolabel = Label(root, text = "Lower Hardness (HB)")
hardlolabel.grid(row=5,column=0)

hardhilabel = Label(root, text = "Higher Hardness (HB)")
hardhilabel.grid(row=5,column=2)

ctelolabel = Label(root, text = "Lower Coefficient of Thermal Expansion (um/mC)")
ctelolabel.grid(row=6,column=0)

ctehilabel = Label(root, text = "Higher Coefficient of Thermal Expansion (um/mC)")
ctehilabel.grid(row=6,column=2)

submit_btn = Button(root, text = "Add Record to Database", command = submit)
submit_btn.grid(row = 7, column = 0, columnspan = 4, pady = 10, ipadx = 200)

searchtitle = Label(root, text = "\n________________________________________________________________________________________________________________________________________________________________________________\n\n\nSEARCH DATBASE FOR MATERIAL: \n Leave blank if value is unknown or unneeded \n Leave checkbox 'min' blank and type input next to 'min' to search for materials with input within range. \n Check box 'min' to search for material where range value is greater than or equal to input \n Check box 'max' to search for material where range value is less than or equal to input \n Leave all blank to look at entire database")
searchtitle.grid(row = 9, column = 0, columnspan = 4)

searchframe = Frame(root)
searchframe.grid(row = 10, column = 0, columnspan = 4)

namesrch = Label(searchframe, text = "Name ")
namesrch.grid(row = 0, column = 0)

nameval = Entry(searchframe, width=30)
nameval.grid(row = 0, column=1, columnspan = 4,ipadx = 82)

'''----------------------------------------------------------------------------------------------------------'''

yieldsearch = Label(searchframe, text = "Yield Strength (MPa)")
yieldsearch.grid(row=1, column = 0)

minvaryield = IntVar()
c1 = Checkbutton(searchframe, text = "Min", variable = minvaryield, onvalue = 1, offvalue = 0)
c1.grid(row=1, column = 1)

minyield = Entry(searchframe, width=20)
minyield.grid(row=1,column=2)

maxvaryield = IntVar()
c2 = Checkbutton(searchframe, text = "Max", variable = maxvaryield, onvalue = 1, offvalue = 0)
c2.grid(row=1, column = 3)
maxyield = Entry(searchframe, width=20)
maxyield.grid(row=1,column=4)

'''--------------------------------------------------------------------------------------------------------------'''
ultsearch = Label(searchframe, text = "Ultimate Tensile Strength (MPa)")
ultsearch.grid(row=2, column = 0)

minvarult = IntVar()
c3 = Checkbutton(searchframe, text = "Min", variable = minvarult, onvalue = 1, offvalue = 0)
c3.grid(row=2, column = 1)

minult = Entry(searchframe, width=20)
minult.grid(row=2,column=2)

maxvarult = IntVar()
c4 = Checkbutton(searchframe, text = "Max", variable = maxvarult, onvalue = 1, offvalue = 0)
c4.grid(row=2, column = 3)

maxult = Entry(searchframe, width=20)
maxult.grid(row=2,column=4)

'''----------------------------------------------------------------------------------------------------------------'''

elosearch = Label(searchframe, text = "Elongation at Yield (%)")
elosearch.grid(row=3, column = 0)

minvarelo = IntVar()
c5 = Checkbutton(searchframe, text = "Min", variable = minvarelo, onvalue = 1, offvalue = 0)
c5.grid(row=3, column = 1)

minelo = Entry(searchframe, width=20)
minelo.grid(row=3,column=2)

maxvarelo = IntVar()
c6 = Checkbutton(searchframe, text = "Max", variable = maxvarelo, onvalue = 1, offvalue = 0)
c6.grid(row=3, column = 3)

maxelo = Entry(searchframe, width=20)
maxelo.grid(row=3,column=4)

'''----------------------------------------------------------------------------------------------------------'''

hardsearch = Label(searchframe, text = "Brinell Hardness (HB)")
hardsearch.grid(row=4, column = 0)

minvarhard = IntVar()
c7 = Checkbutton(searchframe, text = "Min", variable = minvarhard, onvalue = 1, offvalue = 0)
c7.grid(row=4, column = 1)

minhard = Entry(searchframe, width=20)
minhard.grid(row=4,column=2)

maxvarhard = IntVar()
c8 = Checkbutton(searchframe, text = "Max", variable = maxvarhard, onvalue = 1, offvalue = 0)
c8.grid(row=4, column = 3)

maxhard = Entry(searchframe, width=20)
maxhard.grid(row=4,column=4)

'''----------------------------------------------------------------------------------------------------------'''

ctesearch = Label(searchframe, text = "Coefficient of Thermal Expansion (um/mC)")
ctesearch.grid(row=5, column = 0)

minvartherm = IntVar()
c9 = Checkbutton(searchframe, text = "Min", variable = minvartherm, onvalue = 1, offvalue = 0)
c9.grid(row=5, column = 1)

mintherm = Entry(searchframe, width=20)
mintherm.grid(row=5,column=2)

maxvartherm = IntVar()
c10 = Checkbutton(searchframe, text = "Max", variable = maxvartherm, onvalue = 1, offvalue = 0)
c10.grid(row=5, column = 3)

maxtherm = Entry(searchframe, width=20)
maxtherm.grid(row=5,column=4)

'''----------------------------------------------------------------------------------------------------------'''
srch_btn = Button(searchframe, text = "Search", command = search)
srch_btn.grid(row = 6, column = 0, columnspan = 5, pady = 5, ipadx = 250)

edittitle = Label(root, text="________________________________________________________________________________________________________________________________________________________________________________\n")
edittitle.grid(row = 11, column = 0, columnspan = 4)

edit_btn = Button(root, text = "Edit or Delete an Entry", command = edit)
edit_btn.grid(row = 12, column = 0, columnspan = 4, pady = 5, ipadx = 210)

mylabels = [edittitle, namelabel, yieldhilabel, yieldlolabel, tenslolabel, tenshilabel, elonghilabel, elonglolabel, hardhilabel, hardlolabel, ctelolabel, ctehilabel, searchtitle, additiontitle, namesrch, yieldsearch, ultsearch, elosearch, hardsearch, ctesearch]
myentries = [name, yieldstrhi, yieldstrlo, ulttensilstrhi, ulttensilstrlo, elongationhi, elongationlo, hardnesshi, hardnesslo, thermcoeffhi, thermcoefflo, nameval, mintherm, minhard, minelo, minult, minyield, maxtherm, maxhard, maxelo, maxult, maxyield]
mychecks = [c1, c2, c3, c4, c5, c6, c7 ,c8 ,c9 ,c10]
mybuttons = [edit_btn, submit_btn, srch_btn]

labelformat(mylabels)
entryformat(myentries)
buttonformat(mybuttons)
checkformat(mychecks)

searchframe.configure(bg = "#42414A")


root.mainloop()
