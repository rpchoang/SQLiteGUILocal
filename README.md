# SQLiteGUILocal

 @ORIGINAL AUTHOR - RONALD HOANG 1/6/2021 rpchoang@gmail.com

 This program gives us an easy to use GUI to explore a Lordstown Motor's material database and its mechanical properties
 Python Program to edit, search, add, and delete from this database, we look at yield str, ultimate tensile str, elongation at yield, hardness, and CTE
 Datbase is based off of SQLite3
 GUI is written in tkinter
 Executable file created with pyinstaller

 COMMAND USED TO COMPILE EXE: 
	"pyinstaller -w -icon=Lordstown.ico --onefile --hidden-import multiprocessing --name LMCMaterialsDatabase SQLiteGUI.py"
 If you are having trouble running the EXE, please make sure you have the ico file in the same folder as your .exe!
 If you are having trouble running the command please make sure you have Python3 downloaded, and using pip from the command window:
	"pip install tkinter"
	"pip install sqlite3"
	"pip install pillow"
s

 ------FEATURES V1.2.0--------
 INSTRUCTIONS TO GET STARTED USING THIS PROGRAM
 	1/13/2021
 - Now connected to Battery and Propulsion team one drive! Multiple people can now use and update the same database. 
 		Please make sure you are synced to the Battery & Propulsion Team general folder. Please check to see if your path to the materials database would be:
 		"C:/Users/<YOUR USENAME>/Lordstown Motors Corp/Battery & Propulsion Team - General/Documents/DATABASE/materials.db"
 		ONLY PEOPLE ON THE PROPULSION TEAM CAN ACCESS THIS DATABASE
 - Created an executable file for easier use! Please ensure that you have the LMCMaterialsDatabase.exe and Lordstown.ico in the same folder anywhere on your computer
 		You can make a shortcut the the datbase exe and leave it on your desktop
 - I don't have a publishing license so Windows Defender will say its protecting your PC, you can click More Info -> Run Anyways

 ------FEATURES V1.0.1--------
 	1/8/2021
 - Added a search page refresh button to see any updates

  ------FEATURES V1.0.0--------
  	1/6/2021
 - Add materials to database, if empty then will leave the corresponding area in the database blank, still able to edit later
 - Search database based on any of the mechanical properties or a combination of any of the properties 
 		Search based on input being in range, or known material property being within bounds we list
 		Set the MIN MAX values of the property, or have the input listed be checked to be in the min max values of the material
 		Leave inputs blank to search 
 		Opens a seperate window for you to explore your search results
 		Refresh button for Search results to see yourself edit, add, or remove entries into the database
 - Edit or Delete an entry based on known ID #
 		New window pops up when button is pressed 
 		Can update individual values or many at once for a single database entry
 		Commit changes and click refresh button on the search window to see the value be updated

 TODO
 - Add more mechanical properties: Density, Thermal Conductivity, Electrical Conductivity, Melting Point, Youngs Modulus, Specific Heat Capacity
 - Implement features to search for either chemical properties/composition or mechanical properties or both
 - Implement a better "close enough" name search instead of just contains
 - Plan to have a less memory intensive way of looking at all entries without having to list them all at once
 - Have a main menu
 - Find more data to add to database
 - Implement Entry box sanity checkers to ensure only correct input is passed through
 - Bug fix refresh button, deleting/adding an entry will sometimes make it so the scrolling window doesn't resize properly but does update the actual database still
