#/usr/bin/python
import getopt, sys
import requests
from lxml import html, etree
from lxml.html.clean import clean_html

def download_posts(post_urls, web_root_url):

	global verbose, list_only, counter
	global index_file_name

	for post_url in post_urls:

		if verbose:
			print 'Downloading', post_url

		page = requests.get(post_url)
		#tree = html.fromstring(page.text)

		#post_date = tree.xpath('//*[@id="single-date"]/text()')[0]		
		##post-1
		post_short_url = str(post_url).replace(web_root_url,'').replace('/','').replace('\\','').replace('*','')
		
		#post_data = tree.text_content().encode('utf8') 
		#post_data = clean_html(page.text)
		tree = etree.HTML(page.text)

		try:
			post_title = tree.xpath('//*[@id="content"]/div[2]/div[1]/h1/text()')[0]
			post_data = tree.xpath('//*[@id="content"]/div[2]')

		except:
			print 'Could not parse the page'
			return

		counter = counter + 1
		file_name = str(counter) + ' ' + post_short_url + '.html'

		if verbose:
			print 'Writing', file_name
		with open(file_name, 'w') as f:
			#f.write(('<html xml:lang="en" xmlns="http://www.w3.org/1999/xhtml"><body>').encode('utf8'))
			for node in post_data:
				s = etree.tostring(node)
				# replace inline image urls; 
				# download images
				f.write(s.encode('utf8'))
				#f.write(post_data.encode('utf8'))
				#f.write(('</body></html>').encode('utf8'))
		#f.close()

		with open(index_file_name, 'a') as i:
			s = ('<li><a href="' + file_name + '">' + post_title + '</a></li>').encode('utf8')
			i.write(s)


def parse_page_urls(url, web_root_url):

	global verbose, list_only, skip

	page = requests.get(url)
	tree = html.fromstring(page.text)

	post_urls = []
	div_num = 2

	while (1==1):
		path = '//*[@id="content"]/div[' + str(div_num).lstrip(' ') + ']/div[1]/h2/a'
		post_url = tree.xpath(path +'/@href')
		if len(post_url) == 0:
			return post_urls
		div_num = div_num + 1
		post_urls.append(post_url)

		if (skip > 0):
			skip = skip - 1		
		else:
			if verbose:
				print 'Found post ', post_url
			
			if (list_only  == False):			
				download_posts(post_url, web_root_url)

	return post_urls

def get_post_urls(url):

	global verbose, list_only

	page_num = 1
	urls = []

	while (1==1):
		page_url = url + '/page/' + str(page_num).lstrip(' ') + '/?order=ASC'
		if verbose:
			print "Parsing " + page_url
		post_urls = parse_page_urls(page_url, url)
		if len(post_urls) == 0:
			return urls;
		urls.append(post_urls)
		page_num = page_num + 1

		  

def scrape(url):

	global verbose, index_file_name, skip, list_only

	if verbose:
		print "Scraping URL: " + url

		# get page links
	
	try:
		if (skip == 0) and (list_only == False):
			with open(index_file_name, 'w') as i:
				i.write(('<html><body><p>' + url + '</p><ul>').encode('utf8'))

		post_urls = get_post_urls(url)
		print 'Found ' + str(len(post_urls)) + ' posts'

		if list_only == False:
			with open(index_file_name, 'a') as i:
				i.write(('</ul></body></html>').encode('utf8'))

	except RuntimeError as e:
		print str(e)


def usage():
	print "Arguments: {http-url} [--List]"

def main():
	# global settings

	global verbose, list_only, skip
	try:
		opts, args = getopt.getopt(sys.argv[2:], "s:lvh")

	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	
	for o, a in opts:
		if o == "-v":
			verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-l", "--list"):
			list_only = True
		elif o in ("-s", "--skip"):
			skip = int(float(a))
		else:
			assert False, "unhandled option"

	url = sys.argv[1]

	if verbose:
		print 'List only: ', list_only
		print 'Skipping' , skip, 'posts'
		print 'Url', url

	scrape(url)

skip = 0
verbose = False
list_only = False
counter = 0
index_file_name = 'index.html'
if __name__ == "__main__":
	main()

