#/usr/bin/python
import getopt, sys
import requests
from lxml import html
from lxml.html.clean import clean_html


def download_posts(post_urls, web_root_url):

	global verbose, list_only, counter

	for post_url in post_urls:

		if verbose:
			print 'Downloading', post_url

		page = requests.get(post_url)
		#tree = html.fromstring(page.text)

		#post_date = tree.xpath('//*[@id="single-date"]/text()')[0]		
		##post-1
		post_short_url = str(post_url).replace(web_root_url,'').replace('/','')
		print web_root_url
		print post_short_url
		#post_data = tree.text_content().encode('utf8') #tree.xpath('//*[@id="content"]/div[2]/text()')
		post_data = clean_html(page.text)

		counter = counter + 1
		file_name = str(counter) + ' ' + post_short_url + '.html'

		f = open(file_name, 'w')
		#f.write(('<html xml:lang="en" xmlns="http://www.w3.org/1999/xhtml"><body>').encode('utf8'))
		f.write(post_data.encode('utf8'))
		#f.write(('</body></html>').encode('utf8'))
		f.close()


def parse_page_urls(url, web_root_url):

	global verbose, list_only

	page = requests.get(url)
	tree = html.fromstring(page.text)

	post_urls = []
	div_num = 2

	while (1==1):
		path = '//*[@id="content"]/div[' + str(div_num).lstrip(' ') + ']/div[1]/h2/a'
		post_url = tree.xpath(path +'/@href')
		if len(post_url) == 0:
			return post_urls
		if verbose:
			print 'Found post ', post_url
		post_urls.append(post_url)
		div_num = div_num + 1

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

	global verbose

	if verbose:
		print "Scraping URL: " + url

		# get page links
	
	try:	
		post_urls = get_post_urls(url)
		print 'Found ' + str(len(post_urls)) + ' posts'

		#if (list_only == False):
		#	download_posts(post_urls)

	except RuntimeError as e:
		print str(e)


def usage():
	print "Arguments: {http-url} [--List]"

def main():
	#global verbose
	#global list_only

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:vl", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    list_only = False
    verbose = False

    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-l", "--list"):
            #output = a
            list_only = True
        else:
            assert False, "unhandled option"
    # ...
    url = args[0]

    if verbose:
    	print 'List only: ', list_only
    scrape(url)

# global settings
verbose = True
list_only = False
counter = 0

if __name__ == "__main__":
    main()

