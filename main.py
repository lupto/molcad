# Choi Lab PyMol Expansion/PDB file designer
# Summer 2017
# Designed by Luke Upton under the guidance of lab members
#
# Description: This script is intended to generate PDB
# layouts of desired molecules upon request.  There are
# built in structures (DNA double helix, H20, H2, tetrahedral carbon).

# Imported Modules
import os
import time

### Initializations ###
global mode  # Operating mode of script
mode = ''
global command# User command
command = ''
global legitimate_command # Indicates if user made a legitimate request in an operating mode
legitimate_command = 0
global generate_command_list
generate_command_list = [["direct", "Direct atomic coordinate entry"],
["helix", "Generates helical structure"],
["tetra", "Generates a tetrahedron"],
["line", "Generates a line"]
]
global modify_command_list
modify_command_list = []
global convert_command_list
convert_command_list = [['atoms pdb -> csv','Copies element and coordinate info into csv'],
['atoms csv -> pdb', 'Creates pdb document based on csv with elements and coordinates'],
['exit', 'Return to starting menu']]
global writefile    # FID for file that is written to in operations
global tempfile		# FID for temporary file in modify operations
global filename		# PDB Filename input by user
filename = ''
global file_array
file_array = []		# Array of all information in file
global atom_end_line # end line for atom block
atom_end_line = 0
global atom_start_line #starting line for atom block
atom_start_line = 0
global debug		# Debug mode switch
debug = 0
global general_command_list # Universal commands
general_command_list = [["view", "View contents of file"],
["exit", "Save and return to starting menu"]
]
global make_new_PDB # Conversion mode:  Signals when a new PDB is needed (csv -> pdb, etc.)
make_new_PDB = 0

### Functions ###


# GENERATE/MODIFY MODE
def write_atom(element, x, y, z):  # write an atom's coordinates to the next atom line in a file
	global atom_end_line
	global atom_start_line
	global file_array
	temp_array = []
	atom_number = 0
	# Shift everything after the end of the atom block
	atom_end_line = atom_end_line + 1
	for i in range(atom_end_line, len(file_array)):
		temp_array.append(file_array[i])
	file_array.append([]) #filler
	for i in range(atom_end_line + 1, len(file_array)):
		file_array[i] = temp_array[i - (atom_end_line + 1)]
	atom_number = atom_end_line - atom_start_line + 1
	file_array[atom_end_line] = ['ATOM', str(atom_number), str(element), 'GLU', 'A', '61', str(x),
	str(y), str(z), '1', '56.14',str(element)]
	
	if (debug == 1):
		print(atom_end_line)
		print(file_array[atom_end_line])
	
def helix(): # Generates Helices along with cartoon view representation
	#print('hi')
	return 0
def direct(): # Direct entry of atoms using element and coordinate
	#print('hi')
	print('\n')
	element = input('Enter element name: ')
	xcoord = input('Enter x coordinate: ')
	ycoord = input('Enter y coordinate: ')
	zcoord = input('Enter z coordinate: ')
	element = element_correction(element)
	print('\n')
	write_atom(element, xcoord, ycoord, zcoord)

# Gets all element names in a format that can be successfully written
def element_correction(element):
	output = '' #Element symbol to be output
	# Carbon
	if (element.lower() == 'carbon') or (element.lower() == 'c'):
		output = 'C'
	# Sulfur
	elif (element.lower() == 'sulfur') or (element.lower() == 's'):
		output = 'S'
	# Phosphorus
	elif (element.lower() == 'phosphorus') or (element.lower() == 'p'):
		output = 'P'
	# Oxygen
	elif (element.lower() == 'oxygen') or (element.lower() == 'o'):
		output = 'O'
	# Hydrogen
	elif (element.lower() == 'hydrogen') or (element.lower() == 'h'):
		output = 'H'
	else:
		output = element   # This could lead to an error if somebody 
							# puts in around a 3 character long element name
	return output
	

# CONVERT MODE 
def write_atoms_to_csv():  # Converts the atomic information in a .pdb to a csv format
	global writefile
	global file_array
	global atom_start_line
	global atom_end_line
	global filename
	output_line = '' # placeholder for output line
	csv_target = '' # Placeholder for csv filename
	filename = ''
	
	while (filename == ''):
		filename = input("Please enter a PDB filename: ")
		filename = filename.strip('.pdb')
		if (os.path.isfile(filename + '.pdb')):
			file_initialization() # Open and access contents of PDB file
		else:
			print('Error: cannot access file')
			time.sleep(1)
			filename = ''
	csv_target = input("\nEnter filename of target .csv file: ")
	csv_target = csv_target.strip('.csv')
	print('Overwriting/creating {0}.csv'.format(csv_target))
	csv_fid = open(csv_target + '.csv', 'w') #Overwrites existing files, creates otherwise
	for i in range(atom_start_line, atom_end_line + 1):
		output_line = '{0},{1},{2},{3}\n'.format(file_array[i][2], file_array[i][6], file_array[i][7],file_array[i][8])
		csv_fid.write(output_line)
	
	csv_fid.close()
	close_files()
	
def write_atoms_from_csv():
	global make_new_PDB
	global writefile
	global file_array
	global atom_start_line
	global atom_end_line
	global filename
	make_new_PDB = 1 # we want a new document here
	csv_target = ''
	filename = ''
	temp_array = [] # array for storing csv info
	
	while(csv_target == ''):
		csv_target = input("\nEnter filename of input .csv file: ")
		csv_target = csv_target.strip('.csv')
		if (os.path.isfile(csv_target + '.csv')):
			csv_fid = open(csv_target + '.csv', 'r')
		else:
			print("Error: cannot find specified file.")
			csv_target = ''
			time.sleep(1)
	while(filename == ''):
		filename = input("\nEnter filename of output .pdb file: ")
		filename = filename.strip('.pdb')
		if (not os.path.isfile(filename + '.pdb')):
			file_initialization()
		else:
			print("Error: cannot overwrite file.")
			filename = ''
			time.sleep(1)
	
	# We can write atoms in now
	temp_array = csv_fid.readlines()
	
	for i in range(0, len(temp_array)):
		temp_array[i] = temp_array[i].strip().split(',')
		write_atom(temp_array[i][0], temp_array[i][1], temp_array[i][2], temp_array[i][3])
	
	    
	csv_fid.close()
	close_files()
	make_new_PDB = 0
		
	
	
	
	
# FILE CONTROL
def file_initialization():  #Opens All necessary files
	global writefile
	global tempfile
	global filename
	global file_array
	filename = filename.strip('.pdb')
	if (mode == 'generate') or ((mode == 'convert') and (make_new_PDB == 1)):
		if (os.path.isfile(filename + '.pdb')):
			print("Error, file exists. Cannot generate.")
			time.sleep(2) # 2 second delay
			mode_select()
		else:
			writefile = open(filename + '.pdb', 'w')
			#tempfile = open(filename + '_temp.pdb', 'w') # For cartoon arrangements
			writefile.write("HEADER		" + filename + "\n")
			writefile.write("TITLE		" + filename + "\n")
			writefile.write("REMARK		Made with PDB File Editor\n")
			writefile.write("REMARK 	2017 Choi Lab, Purdue University\n")
			writefile.write("ORIGX1      1.000000  0.000000  0.000000        0.00000\n")
			writefile.write("ORIGX2      0.000000  1.000000  0.000000        0.00000\n")
			writefile.write("ORIGX3      0.000000  0.000000  1.000000        0.00000\n")
			writefile.write("SCALE1      0.010163  0.000000  0.006427        0.00000\n")
			writefile.write("SCALE2      0.000000  0.015002  0.000000        0.00000\n")
			writefile.write("SCALE3      0.000000  0.000000  0.015381        0.00000\n")
	elif (mode == 'modify'):
		if(os.path.isfile(filename + '.pdb')):
			writefile = open(filename + '.pdb', 'r+') #Opens output file for reading and writing
			#if (mode == 'modify'):
				#tempfile = open(filename + '_temp.pdb', 'w') #Establishes a clean temporary file
		else:
			print("Error, file does not exist.")
			time.sleep(2)
			mode_select()
	elif ((mode == 'convert') and (make_new_PDB == 0)):
		#print(filename)
		if(os.path.isfile(filename + '.pdb')):
			writefile = open(filename + '.pdb', 'r+') #Opens output file for reading and writing
			#if (mode == 'modify'):
				#tempfile = open(filename + '_temp.pdb', 'w') #Establishes a clean temporary file
		else:
			print("Error, file does not exist.")
			time.sleep(2)
			mode_select()
	writefile.close()
	writefile = open(filename.strip('.pdb') + ".pdb", 'r+')  # Put writefile in editable format
	get_data()
	if (debug == 1):
		print(file_array)
		

def close_files():  #Closes all opened files to prevent I/O Errors
	global writefile
	global tempfile
	global atom_start_line
	global atom_end_line
	atom_start_line = 0  # Reset atom block markers to original conditions
	atom_end_line = 0
	if (mode != 'debug'):
		# write edits to file
		rewrite()
		writefile.close()

def rewrite():  # Overwrites existing file
	global file_array
	
	# Erase
	writefile.seek(0,0)
	for i in range(0, len(file_array)):
		for j in range(0, len(file_array[i])):
			writefile.write('\t\t\t')
		writefile.write('\n')
	
	# Rewrite
	writefile.seek(0,0)
	for i in range(0, len(file_array)):
		if(file_array[i] != []):
			if(file_array[i][0] == 'ATOM'):
				string_holder = '{0:<6}{1:>5} {2:>4} {3:>3} {4:<4}{5}   {6:>8}{7:>8}{8:>8}{9:>6}{10:>6}           {11:<2}'.format(
					file_array[i][0], file_array[i][1], file_array[i][2], file_array[i][3], file_array[i][4], file_array[i][5], file_array[i][6],
					file_array[i][7], file_array[i][8], file_array[i][9], file_array[i][10], file_array[i][11])
								#ATOM  #Number #Name  #Res   #RS#       #x   #y    #z    #Occ  #Temp             #Element
				writefile.write(string_holder)
				if(debug == 1):
					print(file_array[i][5])
					print(string_holder)
					time.sleep(2)
		for j in range(0, len(file_array[i])):
			
			if(file_array[i][0] != 'ATOM'):
				writefile.write(file_array[i][j])
				writefile.write('    ')
		if(i != len(file_array)-1):
			writefile.write('\n')
	if (mode == 'generate') or ((mode == 'convert') and (make_new_PDB == 1)):
		writefile.write('MASTER      336    0    1    9   10    0    1    6 2822    4    4   24   \n')
		writefile.write('END')
	
	
	
	
		
def get_data():  # Grabs all information from PDB file
	global file_array
	global atom_end_line
	global atom_start_line
	file_array = []  # Clear array
	writefile.seek(0,0) # go to beginning of file
	eof = 0
	
	while (eof == 0):
		file_array.append(writefile.readline().strip().split()) # read line by line
		#print(file_array[len(file_array) - 1])
		#time.sleep(1)
		if(file_array[len(file_array) - 1] == []):
			eof = 1
	
	#find atom information
	for i in range(0, len(file_array)):
		if(file_array[i] != []):
			if(file_array[i][0] == 'ATOM'):
				atom_end_line = i
				if(debug == 1):
					print("Found atom at line " + str(atom_end_line))
				if(atom_start_line == 0):
					atom_start_line = i
		elif((file_array[i] == [])and(atom_start_line == 0)):
			# No atoms in file yet
			atom_start_line = 10
			atom_end_line = 9
			
	if (debug == 1):
		print("Atom start line: " + str(atom_start_line))
		print("Atom end line: " + str(atom_end_line))
		print("Number of atoms: " + str(int(atom_end_line) - int(atom_start_line) + 1))
	

def view():  # Displays contents of file_array
	global file_array
	i = 0
	while(file_array[i] != []):
		for j in range(0, len(file_array[i])):
			print(file_array[i][j], end = "\t")
		print('\n')
		i = i + 1
	
	
	
	

# PROMPT OPERATION
def prompt_command(): #prompts user for command
	global legitimate_command
	legitimate_command = 0
	while(legitimate_command != 1): # Keep running until user enters command
		if (debug == 1):
			command = input('debug >>')
		else:
			command = input('>>')
		check_command(command)
	


def check_command(command):  # Checks if a user command is correct.  If correct, initiates procedure
	#print(command)
	if (command == 'help'):
		global legitimate_commmand
		legitimate_command = 1
		help()
	if (command == 'exit'):
		global mode
		global filename
		if (mode != 'convert'):
			close_files()
		make_new_PDB = 0  # Prevents i/o error with convert mode
		legitimate_command = 1
		mode = ''
		filename = ''
		mode_select()
	if (command == 'view'):
		legitimate_command = 1
		view()
	elif (mode == 'generate') or (mode == 'modify'):
		if(command == 'direct'):
			legitimate_command = 1
			direct()
		elif(command == 'helix'):
			legitimate_command = 1
			helix()
	elif (mode == 'convert'):
		if(command == 'atoms pdb -> csv'):
			legitimate_command = 1
			write_atoms_to_csv()
		if(command == 'atoms csv -> pdb'):
			legitimate_command = 1
			write_atoms_from_csv()
			
def help():	# Help command for each mode
	if (mode == 'generate'):
		helplist = generate_command_list
	elif (mode == 'modify'):
		helplist = modify_command_list
		for i in range(0, len(generate_command_list)):
			modify_command_list.append(generate_command_list[i])
	elif (mode == 'convert'):
		helplist = convert_command_list
	
	#Print help menu
	print(mode + " mode command list:\n\n")
	if (debug == 1):
		print("\n\nMode specific commands:")
	for i in range(0, len(helplist)):
		print(helplist[i][0] + " - " + helplist[i][1])
	if (mode != 'convert'):
		if (debug == 1):
			print("\n\nUniversal Commands:")
		for i in range(0, len(general_command_list)):
			print(general_command_list[i][0] + " - " + general_command_list[i][1])	
		print("\n")
	
def mode_select(): #User selects mode
	global mode
	global filename
	while ((mode != 'generate')and(mode != 'modify')and(mode != 'convert')):
		if (mode == 'exit'):
			quit()
		os.system('cls')
		print("User modes:\n")
		print("generate - Generate new PDB file.\n")
		print("modify - add atoms/structures to existing PDB file.\n")
		print("convert - convert atomic layout to spreadsheet containing\nelement and coordinates.\n")
		print("debug - enter/exit debug mode\n")
		print("exit - exit program\n")
		if (debug == 1):
			mode = input("debug >>")
		else:
			mode = input(">>")
		if(mode == 'debug'):
			global debug
			debug = not debug
			mode = ''
	# User has selected a mode
	os.system('cls')  # Clear Screen
	print("Welcome to " + mode + " mode.\n\n")
	if (mode != 'convert'):
		filename = input("Please enter a target filename: ")
		file_initialization() # Open files for appropriate modifications
	print("\nType 'help' to access a listing of commands.\n")
	prompt_command()
	
		
	
	
### MAIN SCRIPT ###

# User Selects a Design Mode
mode_select()

	
	
	
