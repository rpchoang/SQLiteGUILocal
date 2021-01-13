from distutils.core import setup
import py2exe
from tkinter import *
from PIL import ImageTk,ImageTk
from tkinter import PhotoImage
from tkinter import ttk
import sqlite3
import os
import sys
import multiprocessing
multiprocessing.set_start_method('spawn')

from multiprocessing.managers import BaseManager

sys.argv.append('py2exe')

setup(
options = { 'py2exe': {'bundle_files': 2, 'compressed': True}},
	windows=[{
		'script':"SQLiteGUI.py",
		'icon_resources': [(1, 'Lordstown.ICO')]
	 }],
	zipfile = None,
	name = "LMC B&P MaterialsDatabase"
)
