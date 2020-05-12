#! python3
# scheduledWebComicDownloader aka sWCD.py - checks websites of web comic, and
# automatically downloads image if site was updated since last visit.

import bs4, os, requests

# Creates directory to play in.
folderName = 'web-comics'
os.makedirs(folderName, exist_ok=True)

# Downloads comic image if not found already in directory.
def check_for_update(comicUrl):

	# Get image filename.
	fileName = os.path.basename(comicUrl)
	
	# Check if today's comic exists in directory.
	if fileName in os.listdir(folderName):
		print('No updates today. Most recent comic is at %s.' % comicUrl)
	
	# Else download today's comic.
	else:
		print('Downloading %s...' % comicUrl)

		res = requests.get(comicUrl)
		res.raise_for_status()
		imageFile = open(os.path.join(folderName, fileName), 'wb')
		for chunk in res.iter_content(100000):
			imageFile.write(chunk)
		imageFile.close()

def get_qwantz_comic():

	# Get today's comic's url.
	site = 'http://www.qwantz.com'
	
	# Get url text to parse for img.
	res = requests.get(site)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	
	# Get image url.
	comicElem = soup.select('.comic')
	comicUrlShort = comicElem[0].get('src')
	comicUrl = site + '/' + comicUrlShort
	
	# Confirm whether there is an img url.
	if comicElem == 0:
		print('Could not find comic element at %s.' % site)

	# Begin download of img with url.
	else:
		check_for_update(comicUrl)
	
def get_xkcd_comic():

	# Get today's comic's url.	
	site = 'https://xkcd.com'
	
	# Get url text to parse for img.
	res = requests.get(site)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	
	# Get image url.
	comicElem = soup.select('#comic > img')
	comicUrlShort = comicElem[0].get('src')
	comicUrl = 'http:' + comicUrlShort
	
	# Confirm whether there is an img url.
	if comicElem == 0:
		print('Could not find comic element at %s.' % site)

	# Begin download of img with url.
	else:
		check_for_update(comicUrl)

get_qwantz_comic()
get_xkcd_comic()