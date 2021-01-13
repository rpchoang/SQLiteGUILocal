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

entry_point = sys.argv[1]
sys.argv.pop()
sys.argv.append('py2exe')
sys.argv.append('q')

setup( console = [entry_point],
options = { 'py2exe': {'bundle_files': 1, 'compressed': True, 'optimize': 2}},
	windows=[{
		'script':"SQLiteGUI.py",
		'icon_resources': [(1, 'Lordstown.ICO')]
	 }],
	zipfile = None,
	name = "LMCDatabase"
)

