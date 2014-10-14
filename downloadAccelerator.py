"""CS 360 Lab 3 Download Accelerator"""
import argparse
import threading
import urlparse


"""called with three strings: threads, url
Output: [URL] [#Threads] [bytes] [seconds]"""


class downloadAccelerator:#(threading.Thread):

	def __init__ (self):
		#threading.Thread.__init__(self)
		self.args = None
		self.threads = 5
		self.file_name = 'index.html'
		self.url = ""
		self.parse_arguments()
		self.seconds = 0.0
		self.bytes = 0

	"""Parse Command line arguments"""
	def parse_arguments(self):
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
		self.file_name = (args.URL).split('/')[-1].strip()



	"""Download file"""
	def download(self):
		threads = []
		#make however many threads were specified
		for i in range(0,self.threads):
			#make thread
			d = DownloadThread(url, file_name)
			#add thread to thread array
			threads.append(d)

		#start the threads
		for t in threads:
			t.start()
		#?
		for t in threads:
			t.join()



"""Downloading Threaded Class"""
class DownloadThread(threading.Thread):
	#Constructor
	def __init__(self, url, file_name):
		self.url = url
		self.file_name = file_name
		threading.Thread.__init__(self)
		self.consumed = False

	
	def run(self):
		#?
		r = requests.get(self.url, stream = True)
		#? 'wb'?
		with open(self.file_name, 'wb') as f:
			f.write(r.content)