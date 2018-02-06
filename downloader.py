from urllib2 import Request, urlopen
import urllib2
from PyPDF2 import PdfFileWriter, PdfFileReader
from StringIO import StringIO
import lxml.html
import re
import multiprocessing
from multiprocessing import Pool
import time
import sys

# Helper function to Download Files
def readlinks(link):
	file_type = 'pdf'
	
# check if PDF file 
# if file is pdf try to connect and download it 
	if link[0].find(file_type) != -1 :
		url =  link[0]
		writer = PdfFileWriter()
		   
		try:
			remoteFile = urlopen(Request(url)).read()
				   
		except:
			return
		
		try:
			memoryFile = StringIO(remoteFile)
			pdfFile = PdfFileReader(memoryFile)
			dummy = pdfFile.getNumPages()
		except:
			return

		
		
		outputStream = open( str(link[1]) + ".pdf" ,"wb")

		# try to write the pdf locally for analysis					 
		for pageNum in xrange(pdfFile.getNumPages()):
			try:
				currentPage = pdfFile.getPage(pageNum)
			except:
				outputStream.close()
				return
		#currentPage.mergePage(watermark.getPage(0))
			try:
				writer.addPage(currentPage)

				writer.write(outputStream)
										   
			except:
				continue
												   
		outputStream.close()

def convert_pdf_to_txt( path):

	fp = file(path+".pdf", 'rb')
	try:
		fp = open(path +".pdf" , "rb")
		sys.stdout.flush()
		rsrcmgr = PDFResourceManager()
		retstr = StringIO()
		codec = 'utf-8'
		laparams = LAParams()
		device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

	except:
		return
		 
	try:
		interpreter = PDFPageInterpreter(rsrcmgr, device)
		password = ""
		maxpages = 0
		caching = True
		pagenos=set()

	except:
		return
								 
	try:
		PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True)
	except:
		return
										    
	try:
		for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
			interpreter.process_page(page)
		
	except:
		return
			 
	try:
		fp.close()
		device.close()
		str = retstr.getvalue()
		retstr.close()
		print path + ".txt "
		print "outputting"
		output = open(path + ".txt", "w")
		output.write(str)
		output.close()
		 
	except:
		return

def reader(fname):
	print fname[0]
	try:
		file = open(fname[0]  , 'r')

	except IOError:
		return
				   
		
	for line in file:
		for keyword in fname[1]:
			match = re.match("(.*) " +keyword+ " (.*?) .*", line , re.M | re.I)
			if match:
				print "file: ", fname[0]
				print match.group(0)
				print match.group(1)
				print match.group(2)

#	for line in file:
#		match = re.match("(.*) merit (.*?) .*", line , re.M | re.I)
#		if match:
#			print fname[0]
#			print match.group(0)
#			print match.group(1)
#			print match.group(2)
	 
	
#			match = re.match("(.*)  Merit (.*?) .*", line , re.M | re.I)
#			if match:
#			print fname [0]
#			print match.group(0)
#			print match.group(1)
#			print match.group(2)
#

#lass that does all of the ttttttttttt and anlysi
class downloader(object):
#constructors
	def __init__(self , sources=[],dicts = {} , files = [] , keywords=[]):
		#urls
		self.sources= sources

		#site names for each source

		self.dicts  = dicts

		#all downloaded files

		self.files  = files

		#keywords 

		self.keywords = keywords

  #add keyword of interest
	def add_keyword(self,key):
		self.keywords.append(key)
  
	#returns nbr of files
	def nbr_files(self):
		return len(self.files)

  # creates sources

	def init_sources(self,items):
		self.sources = items
  # necessary repository informations 

	def set_links(self, dicts):
		self.dicts = dicts
  
  #print out sources

	def print_sources(self):
		print self.sources
  
	# add new source
	def add_sources(self,item):
		self.sources.append(item)

	#returns list of sources
	def get_sources(self):
		return self.sources

	# serial downloading of files
	
	
# download in serial mode
	def download_all(self):
		for url in self.sources:
			connection = urllib2.urlopen(url)
			dom =  lxml.html.fromstring(connection.read())
			str1 = 'pdf'
			site = self.dicts[url]
			for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
				if link.find(str1) != -1 :
					url = site + link + '.pdf'
					print url

					writer = PdfFileWriter()

					try:
						remoteFile = urlopen(Request(url)).read()

					except:
						continue

					memoryFile = StringIO(remoteFile)
					pdfFile = PdfFileReader(memoryFile)
					outputStream = open(link[13] +".pdf","wb")
	  
					for pageNum in xrange(pdfFile.getNumPages()):
						currentPage = pdfFile.getPage(pageNum)

			       #currentPage.mergePage(watermark.getPage(0))
						try:

							writer.addPage(currentPage)
							writer.write(outputStream)
					   
						except:
							continue
							   
							   
					outputStream.close()

  #local class member that creates pdf files from source
	def readlinks(self,link):
		file_type = 'pdf'
		if link.find(file_type) != -1 :
			url =  link
			writer = PdfFileWriter()

			try:
				remoteFile = urlopen(Request(url)).read()
	 
			except:
				return
		   
			memoryFile = StringIO(remoteFile)
			pdfFile = PdfFileReader(memoryFile)
	  
			for pageNum in xrange(pdfFile.getNumPages()):
				currentPage = pdfFile.getPage(pageNum)
			   
#currentPage.mergePage(watermark.getPage(0))
				try:
					writer.addPage(currentPage)
					outputStream = open("output.pdf","wb")
					writer.write(outputStream)
					 
				except:
					continue
							   
							   
			outputStream.close()

# download pdf's in parallel
	def download_parallel(self):
		links = []
		ids  =[]
		id=0
		for url in self.sources:
 
			print url

			connection = urllib2.urlopen(url)
			dom =  lxml.html.fromstring(connection.read())
			file_type = 'pdf'
			site = self.dicts[url]
      			
			for link in dom.xpath('//a/@href'):
				if link.find(file_type) != -1 :
					url =  site + link + '.pdf'
					tmp=[url,id]	
					self.files=[str(id) + ".pdf"]
					links.append(tmp)
					id = id + 1
	
#print len(links)
			pool = Pool(processes=multiprocessing.cpu_count())
			pool.map(readlinks,links)



	def analyzer(self, key):
		nbr_matches= 0
		for i in range(1,2):
			print i 
			print self.keywords[key]

			f=open(str(i) + ".pdf","r")
			Match = False 
			pattern='(.*) are (.*?) .*'
			for line in f:
				if re.match(r'(.*) are (.*?) .*' ,line, re.M | re.I):
					print "match"
					if not(Match):
						nbr_matches = nbr_matches + 1
						Match = True

					print line


#class with its own downloader instance
class analyzer():
	def __init__(self):
		
		self.downloader= downloader()

#let the top classes defines these member functions	
	def __getitem__(self,idx):
		return 0

#let the top classes defines these member functions	
	def __len__(self):
		return 0

#create urls instance
urls = analyzer()
sources = ['http://arxiv.org/list/cond-mat/1301?show=1245'  ,
					 'http://arxiv.org/list/cond-mat/1302?show=1273'  ,
					 'http://arxiv.org/list/cond-mat/1303?show=1295' ,
					 'http://arxiv.org/list/cond-mat/1304?show=1318' ,
					 'http://arxiv.org/list/cond-mat/1305?show=1270' ,
					 'http://arxiv.org/list/cond-mat/1306?show=1187' ,
					 'http://arxiv.org/list/cond-mat/1307?show=1458' ,
					 'http://arxiv.org/list/cond-mat/1308?show=1172' ,
					 'http://arxiv.org/list/cond-mat/1309?show=1352' ,
					 'http://arxiv.org/list/cond-mat/1310?show=1374' ,
					 'http://arxiv.org/list/cond-mat/1311?show=1204' ,
					 'http://arxiv.org/list/cond-mat/1312?show=1227' 
						]
#needed to match urls 
#it changes from source to source
dicts = {'http://arxiv.org/list/cond-mat/1301?show=1245':'http://arxiv.org',
				 'http://arxiv.org/list/cond-mat/1302?show=1273' :'http://arxiv.org',
				 'http://arxiv.org/list/cond-mat/1303?show=1295' :'http://arxiv.org',	
				 'http://arxiv.org/list/cond-mat/1304?show=1318' :'http://arxiv.org',
				 'http://arxiv.org/list/cond-mat/1305?show=1270' :'http://arxiv.org',
				 'http://arxiv.org/list/cond-mat/1306?show=1187' :'http://arxiv.org', 
				 'http://arxiv.org/list/cond-mat/1307?show=1458' :'http://arxiv.org',
				 'http://arxiv.org/list/cond-mat/1308?show=1172' :'http://arxiv.org',
				 'http://arxiv.org/list/cond-mat/1309?show=1352' :'http://arxiv.org',
				 'http://arxiv.org/list/cond-mat/1310?show=1374' :'http://arxiv.org',
				 'http://arxiv.org/list/cond-mat/1311?show=1204' :'http://arxiv.org',
				 'http://arxiv.org/list/cond-mat/1312?show=1227' :'http://arxiv.org'
				}


if __name__ == '__main__':
	urls.downloader.init_sources(sources)
	urls.downloader.set_links(dicts)
	urls.downloader.print_sources()

	tag=0
	pool  = Pool(processes= multiprocessing.cpu_count())
	for source in urls.downloader.sources:
		print "reading and analyzing from this source ", source 
		connection = urllib2.urlopen(source)
		dom =  lxml.html.fromstring(connection.read())

		links=[]

		str1 = 'pdf'
		for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
			if link.find(str1) != -1 :
				url = urls.downloader.dicts[source] + link + '.pdf'
				urls.downloader.files.append(url)
				tag=tag + 1
				tmp=[url,tag]
				links.append(tmp)
				urls.downloader.files.append(tmp)
	 
		print 'reading links' 	  
		pool.map(readlinks,links)

#download pdfs and convert txt

#pool= Pool(processes= multiprocessing.cpu_count())
		print "converting pdfs into txt files: avoid this by downloading html"
		pool.map(convert_pdf_to_txt, urls.downloader.files , chunksize=1)

#create files for analysis
#each file has its own keywords 

		print "adding keyword : Merit"
		urls.downloader.add_keyword('Merit')
		
		buffer_files = []

		for i in range(1 , len(urls.downloader.files)):
			string = str(i) + ".txt"
      #add files and keyword(s) as desired
			tmp = [string,urls.downloader.keywords]
			buffer_files.append(tmp)

		pool.map(reader, buffer_files)



