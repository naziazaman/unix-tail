import argparse
import time

BLOCK_SIZE = 1024

def get_last_n_lines(file_name, n = 10):
	'''
	returns the last n lines of the given file
	'''
	with open(file_name) as f:
		f.seek(0, 2)
		file_size = f.tell()

		lines_to_read = n
		block_read = -1
		blocks = []

		while lines_to_read > 0 and file_size > 0:
			if file_size < BLOCK_SIZE:
				# file is shorter than the block size
				# so, move the pointer back at the begining
				# and read the entire file
				f.seek(0, 0)
				blocks.append(f.read(file_size))
			else:
				# read the block from end
				f.seek(block_read * BLOCK_SIZE, 2)
				blocks.append(f.read(BLOCK_SIZE))
			# count the lines read so far and update the 
			# lines need to read counter
			lines_to_read -= blocks[-1].count('\n')
			# reduce the file size
			file_size -= BLOCK_SIZE
			# increase the block counter backwards 
			block_read -= 1
		return '\n'.join(''.join(blocks).split('\n')[-n:])

def get_last_n_characters(file_name, n):
	'''
	returns the last n characters of the given file
	'''
	with open(file_name) as f:
		f.seek(0, 2)
		file_size = f.tell()
		
		# move the pointer at the last n bytes if 
		# file size is bigger than bytes (size) else
		# move the pointer at the beginning of the file
		f.seek(-n, 2) if file_size >= n else f.seek(0, 0)
		return f.read()

def get_lines_except_first_n(file_name, n):
	'''
	returns all the lines except the first n lines
	'''
	with open(file_name) as f:
		while n > 0:
			try:
				# skip the first n lines
				next(f)
				n -= 1
			except StopIteration:
				break
		lines = [line for line in f ]
		return ''.join(lines)


def monitor_file(file_name):
	'''
	monitors the given file for changes and performs tail 
	operation if needed
	'''
	print get_last_n_lines(file_name)

	with open(file_name) as f:
		f.seek(0, 2)
		while True:
			current_position = f.tell()
			lines_added = f.read()
			if lines_added:
				# display the newly added lines if any
				print lines_added
			else:
				# return the pointer back to the current poistion
				f.seek(current_position)
				time.sleep(0.5)

def tail():
	parser = argparse.ArgumentParser()

	parser.add_argument("file_name", help='filename on which tail should be performed')
	parser.add_argument("-n", "--lines", help='display the last lines')
	parser.add_argument("-c", "--chars", help='display the last chars')
	parser.add_argument("-s", "--skip", help='display the all lines except first n')
	parser.add_argument("-f", "--follow", help='monitor the file for changes', action='store_true')

	args = parser.parse_args()
	
	file_name = args.file_name
	if args.lines:
		print get_last_n_lines(file_name, int(args.lines))
	elif args.chars:
		print get_last_n_characters(file_name, int(args.chars))
	elif args.skip:
		print get_lines_except_first_n(file_name, int(args.skip))
	elif args.follow:
		monitor_file(file_name)
	else:
		print get_last_n_lines(file_name)

if __name__ == '__main__':
	tail()
