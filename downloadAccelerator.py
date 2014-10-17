"""CS 360 Lab 3 Download Accelerator"""
import argparse
import threading
import requests
import os
import urlparse
import time
#import wget

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


	"""Parse Command line arguments"""
	def parse_arguments(self):
		#print "PARSING ARGUMENTS!"
		#setup parser
		parser = argparse.ArgumentParser()
		#add parse for # of threads
		parser.add_argument('-n', '--number', type = int, action = 'store')
		#add parse for URL
		parser.add_argument('url',type = str, action = 'store')

		
		#actually parse arguments
		args = parser.parse_args()
		#get the # of threads
		self.threads = args.number
		#get URL
		self.url = args.url
		#get file storage location from URL
		#split the string according to '/' delim and get the last in the array
		self.file_name = (args.url).split('/')[-1].strip()
		#if an empty string then make it index.html for the file name
		if self.file_name == "":
			self.file_name = "index.html"
		#print self.file_name

		#? Does what exactly: what's the file path it follows?
		#if not os.path.exists(self.URL):
		#	os.makedirs(self.URL)




	"""Download file"""
	def download(self):

		response = requests.head(self.url)
		self.bytes = response.headers["content-length"]
		bytes_per_thread = int(self.bytes)/self.threads

		#check if division wasn't clean and needs a some more bytes
		#for last run through
		add_bytes_at_end = 0
		if (int(self.bytes)%self.threads) != 0:
			add_bytes_at_end = int(self.bytes)%self.threads + 1

		#starting byte for each thread
		start_byte = 0
		threads_array = []
		#print "FOR LOOP",len(threads_array)
		#make however many threads were specified
		for i in range(0,self.threads):
			#check if we're on the last thread and add extra bytes
			if i == (self.threads - 1):
				bytes_per_thread = bytes_per_thread + add_bytes_at_end
			#make thread
			d = DownloadThread(self.url, self.file_name, start_byte, bytes_per_thread)
			#print "\nthread",i
			#add to start_byte so next one starts at correct location
			start_byte = start_byte + bytes_per_thread
			#add thread to thread array
			threads_array.append(d)
		
		#start timer
		start_time = time.time()


		#start the threads
		for t in threads_array:
			t.start()
		#
		for t in threads_array:
			t.join()


		#stop timer
		self.seconds = time.time()-start_time

		with open(self.file_name, 'wb') as f:
			for t in threads_array:
				f.write(t.content)

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
		self.content = None
		self.run()

	
	def run(self):
		#make range
		end_byte = self.start_byte + self.bytes - 1

		#print "\nstart_byte:",self.start_byte,"end_byte:",end_byte,"\n"

		headers = { "Range" : "bytes=%s-%s" % (self.start_byte, end_byte), "Accept-Encoding" : "identity"}
		response = requests.get(self.url, headers = headers)
		self.content = response.content
	

		


"""	def write(self):
		#
		with open(self.file_name, 'wb') as f:
			f.write(response.content)"""




if __name__ == '__main__':
	#initialize Object
	download = downloadAccelerator()
	#parse arguments
	download.parse_arguments()
	#start download
	download.download()
	download.print_out()