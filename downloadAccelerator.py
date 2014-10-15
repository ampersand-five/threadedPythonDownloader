"""CS 360 Lab 3 Download Accelerator"""
import argparse
import threading
import requests
import os
import urlparse
import time

"""called with three strings: threads, url
Output: [URL] [#Threads] [bytes] [seconds]"""


class downloadAccelerator:#(threading.Thread):

	def __init__ (self):
		#threading.Thread.__init__(self)
		self.args = None
		self.threads = 5
		self.file_name = ""
		self.url = ""
		self.seconds = 0.0
		self.bytes = 0
		#parse arguments
		self.parse_arguments()
		#start download
		self.download()
		self.print_out()

	"""Parse Command line arguments"""
	def parse_arguments(self):
		print "PARSING ARGUMENTS!"
		sys.stdout.write("PARSING ARGUMENTS!")
		#setup parser
		parser = argparse.ArgumentParser()
		#add parse for # of threads
		parser.add_argument('-n', '--number', type = int, action = 'store')
		#add parse for URL
		parser.add_argument('url', '--URL', metavar = 'URL', type = str, action = 'store')

		
		#actually parse arguments
		args = parser.parse_args()
		#get the # of threads
		self.threads = args.number
		#get URL
		self.url = args.URL
		#get file storage location from URL
		#split the string according to '/' delim and get the last in the array
		self.file_name = (args.URL).split('/')[-1].strip()
		#if an empty string then make it index.html for the file name
		if self.file_name == "":
			self.file_name = "index.html"

		#? Does what exactly: what's the file path it follows?
		#if not os.path.exists(self.URL):
		#	os.makedirs(self.URL)




	"""Download file"""
	def download(self):

		response = requests.header(self.url)
		self.bytes = response.headers["content-length"]
		bytes_per_thread = self.bytes/self.threads

		#check if division wasn't clean and needs a some more bytes
		#for last run through
		add_bytes_at_end = 0
		if (self.bytes%self.threads) != 0:
			add_bytes_at_end = self.bytes%self.threads

		#starting byte for each thread
		start_byte = 0
		threads_array = []
		#make however many threads were specified
		for i in range(0,self.threads_array):
			#check if we're on the last thread and add extra bytes
			if i == (len(self.threads_array) - 1):
				bytes_per_thread = bytes_per_thread + add_bytes_at_end
			#make thread
			d = DownloadThread(url, file_name, start_byte, bytes_per_thread)
			#add to start_byte so next one starts at correct location
			start_byte = start_byte + bytes_per_thread
			#add thread to thread array
			threads_array.append(d)

		#start timer
		start_time = time.time()
		#start the threads
		for t in threads_array:
			t.start()
		#?
		for t in threads_array:
			t.join()
			t.write()

		#clock timer
		self.seconds = time.time()-start_time

	def print_out(self):

		"""Output: [URL] [#Threads] [bytes] [seconds]"""
		print self.url," ",self.threads," ",self.bytes," ",self.seconds










"""Downloading Threaded Class"""
class DownloadThread(threading.Thread):
	#Constructor
	def __init__(self, url, file_name, start_byte, bytes_total):
		self.url = url
		self.file_name = file_name
		threading.Thread.__init__(self)
		self.start_byte = start_byte
		self.bytes = bytes_total
		self.response
		self.run()

	
	def run(self):
		#make range
		end_byte = self.start_byte + bytes

		#?
		headers = { "Range" : "bytes=%s,%s" % (self.start_byte, end_byte), "Accept-Encoding" : "identity"}
		response = requests.get(url, headers=headers)
		


	def write(self):
		#? write binary
		with open(self.file_name, 'wb') as f:
			f.write(response.content)