import random
import hashlib
import os
import time

#Welcome message to display when file is run
welcome = '''
 _   _           _       _____                _             
| | | |         | |     /  __ \              | |            
| |_| | __ _ ___| |__   | /  \/_ __ __ _  ___| | _____ _ __ 
|  _  |/ _` / __| '_ \  | |   | '__/ _` |/ __| |/ / _ \ '__|
| | | | (_| \__ \ | | | | \__/\ | | (_| | (__|   <  __/ |   
\_| |_/\__,_|___/_| |_|  \____/_|  \__,_|\___|_|\_\___|_|   
                                                            


For a list of commands, type: "help"
                                                            '''

os.system('clear')
print(welcome)
current_algorithm = ''
current_dictionary = '/usr/share/dict/words'
current_input_file = ''
current_output_file = ''
verbose = False
output_file = False
input_file = False


def status():
	print('\nDicionary file: ', current_dictionary)
	print('Algorithm: ', current_algorithm)
	if verbose is True:
		print('Verbose: on')
	else:
		print('Verbose: off')
	print('Output file: ', current_output_file)
	print('Input file: ', current_input_file, '\n')

help_info = '''
	To crack a hash, type: crack
	To get a list of the supported hash algorithms, type: algorithms
	To change your settings, type: settings
	To get the current status of your settings, type: status
	To exit the program, type: c
	'''

supported_algorithms = 'MD5, SHA256, SHA512'

def make_output_file(word):
	try:
		f = open(current_output_file + '.txt', "x")
	except FileExistsError:
		exists = input('File already exists, replace it? (y/n) ')
		if exists == 'y' or exists == 'Y':
			f = open(current_output_file + '.txt', 'w+')
			f.write('Word is: {}'.format(word))
			f.close()
			print('\nEverything was written to file succesfully!')
		elif exists == 'n' or exists == 'N':
			print('Please change the output file name in settings')	
	else:
		f.write('Word is: {}'.format(word))
		f.close()

def verbose_and_input_file(chosen_algorithm):

	m = 0
	n = 0

	try:
		input_hashes = open(current_input_file).read().splitlines()
	except FileNotFoundError:
		print('File does not exist\n')
	else:	
		for i in input_hashes:
			start = time.time()
			print('Hashes to calculate: {}'.format(len(input_hashes) - m))
			m += 1
			salt = input('Salt: ')
			l = i.lower()
			for k in words:
				n += 1
				j = bytes(k + salt, 'utf-8')
				hashed = getattr(hashlib, chosen_algorithm)(j).hexdigest()
				print(hashed)
				if hashed == l:
					end = time.time()
					print('\nHash found, the password is: ', k)
					print('\nTime took to complete: ', (end-start))
					print('Words tried: ', n)
					if output_file is True:
						make_output_file(k)
						break
					else:
						break

def verbose_only(chosen_algorithm):

	hash_to_crack = input('Hash to crack: ').lower()
	salt = input('Salt: ')

	start = time.time()
	for i in words:
		n += 1
		j = bytes(i + salt, 'utf-8')
		hashed = getattr(hashlib, chosen_algorithm)(j).hexdigest()
		# Verbose could be checked here and improve readability but would likely slow down the program
		print(hashed)
		if hashed == hash_to_crack:
			end = time.time()
			print('\nHash found, the password is: ', i)
			print('\nTime took to complete: ', (end-start))
			print('Words tried: ', n)
			if output_file is True:
				make_output_file(i)
				break
			else:
				break

def input_file_only(chosen_algorithm):

	m = 0
	n = 0
	try:
		input_hashes = open(current_input_file).read().splitlines()
	except FileNotFoundError:
		print('File does not exist\n')
	else:
		for i in input_hashes:
			start = time.time()
			print('Hashes to calculate: {}'.format(len(input_hashes) - m))
			m += 1
			salt = input('Salt: ')
			l = i.lower()
			for k in words:
				n += 1
				j = bytes(k + salt, 'utf-8')
				hashed = getattr(hashlib, chosen_algorithm)(j).hexdigest()
				if hashed == l:
					end = time.time()
					print('\nHash found, the password is: ', k)
					print('\nTime took to complete: ', (end-start))
					print('Words tried: ', n)
					if output_file is True:
						make_output_file(k)
						break
					else:
						break

def simple_crack(chosen_algorithm):

	n = 0

	hash_to_crack = input('Hash to crack: ').lower()
	salt = input('Salt: ')

	start = time.time()
	for i in words:
		n += 1
		j = bytes(i + salt, 'utf-8')
		hashed = getattr(hashlib, chosen_algorithm)(j).hexdigest()
		if hashed == hash_to_crack:
			end = time.time()
			print('\nHash found, the password is: ', i)
			print('\nTime took to complete: ', (end-start))
			print('\nWords tried: ', n)
			if output_file is True:
				make_output_file(i)
				break
			else:
				break

# Crack the hash
def crack(chosen_algorithm):
	
	# Loop over dictionary file

	if verbose is True and input_file is True:
		verbose_and_input_file(chosen_algorithm)
	elif verbose is True and input_file is not True:
		verbose_only(chosen_algorithm)
	elif verbose is not True and input_file is True:
		input_file_only(chosen_algorithm)
	else:
		simple_crack(chosen_algorithm)
					
# Main
while True:
	
	try:
		beginning = input('> ')
	except KeyboardInterrupt:
		print('')
		exit()

	if beginning == 'help':
		print(help_info)
	elif beginning == 'settings':
		print('''
Type: "help" + "command name" for a list of available options.

1. Algorithm
2. Dicionary
3. Verbose
4. Input file
5. Output file\n''')

		# Change settings category 
		while True:
			try:
				choice = input('settings > ')
			except KeyboardInterrupt:
				print('')
				exit()

			if choice == '1':
				current_algorithm = input('settings/algorithm > ').lower()
			elif choice == '2':
				current_dictionary = input('settings/dictionary > ')
			elif choice == '3':
				if verbose == True:
					verbose = False
				else:
					verbose = True
				print('Verbose: ', str(verbose))
			elif choice == '4':
				input_file_choice = input('Would you like to use an input file? (y/n) ')
				if input_file_choice == 'y' or input_file_choice == 'Y':
					while True:
						current_input_file = input('settings/Input-file name > ')
						if current_input_file[-4:] != '.txt':
							print('You must enter a ".txt" file.')
						else:
							input_file = True
							break
				else:
					print('')
			elif choice == '5':
				output_file_choice = input('Would you like to use an output file? (y/n) ')
				if output_file_choice == 'y' or output_file_choice == 'Y':
					output_file = True
					current_output_file = input('settings/Output-file name > ')
				else:
					print('')
			elif choice == 'list':
				print('''
Type: "help" + "command name" for a list of available options.

1. Algorithm
2. Dicionary
3. Verbose
4. Input file
5. Output file\n''')
			elif choice == 'status':
				status()
			elif choice == 'c' or choice == 'x':
				break
			elif choice == 'help':
				print('Type: "help command_name" for help')
			elif choice == 'help input file' or choice == 'help Input file' or choice == 'help 4':
				print('''
Input file: a file containing several hashes to be cracked.
Make sure there is one hash per line.\n''')
			elif choice == 'help output file' or choice == 'Outpute file' or choice == 'help 5':
				print('''
Output file: the file that will be created with the final results
of the program.\n''')
			elif choice == 'help dictionary' or choice == 'help Dicionary' or choice == 'help 2':
				print('''
Dictionary: directory of the dictionary file that you would like
to use to compute the hash/hashes provided.\n''')
			elif choice == 'help verbose' or choice == 'help Verbose' or choice == 'help 3':
				print('''
Verbose: Show all the hashes being calculated live.''')
			elif choice == 'help algorithm' or choice == 'help Algorithm' or choice == 'help 1':
				print('''
Algorithm: which hashing algorithm should the program use to crack the hash.
This needs to be the same algorithm as the hash you are trying to crack''')
			else:
				print('Not an option')
	elif beginning == 'crack':
		# Hash to crack

		# Open dictionary file if it exists
		try:
			words = open(current_dictionary).read().splitlines()
		except FileNotFoundError:
			print('Invalid dictionary directory\n')

		# Run crack() based on algorithm
		if current_algorithm == 'md5':
			crack('md5')
			#print('Hash was not found')
		elif current_algorithm == 'sha256':
			crack('sha256')
			#print('Hash was not found...')
		elif current_algorithm == 'sha512':
			crack('sha512')
			
			#print('Hash was not found...')
		else:
			print('Hash algorithm not supported, type: "algorithms", to check the supported hash functions')

	elif beginning == 'algorithms':
		print(supported_algorithms)
	elif beginning == 'clear':
		os.system('clear')
		print(welcome)
	elif beginning == 'c':
		exit()
	elif beginning == 'status':
		status()
		
	elif beginning == 'info':
		print('''
Hash cracker takes a hash and appends the provided salt to it.
After that, it loops through a dictionary file and hashes 
every single word using the hash algorithm provided. After
each hash, it checks whether it matches the hash to be cracked.\n''')
	else:
		print('Unknown command')
