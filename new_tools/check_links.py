import requests
from lxml import html
import json

base_url = 'http://www.birthtools.org'
all_links = {base_url: None}

def get_page_links(url):
	page = requests.get(url)
	webpage = html.fromstring(page.content)

	return webpage.xpath('//a/@href')

def clean_page_links(links, base_url):
	new_links = []
	for link in links:
		if(len(link) == 0 or link[0] == '#'):
			continue
		elif(link[:8] == 'http:///'):
			link = 'http://' + link[9:]
		elif(link[:4] != 'http'):
			if(link[0] == '/'):
				link = link[1:]
			new_link = base_url + '/' + link
		else:
			new_link = link

		if(new_link[-1] == '/'):
			new_link = new_link[:-1]

		new_links.append(new_link)

	return new_links

def check_link(link):
	try:
		r = requests.head(link)
		return str(r.status_code)
	except requests.ConnectionError:
		return 'Connection Error'
	except requests.exceptions.InvalidURL:
		return 'invalid URL'

def unchecked_links(links):
	for link in links:
		if(links[link] is None):
			return True
	return False

def merge_links(links, new_links):
	for new_link in new_links:
		if new_link not in links:
			links[new_link] = None
	return links

def check_links(links, base_url):
	while(unchecked_links(links)):
		for link in list(links):
			if(links[link] == None):
				links[link] = check_link(link)
				if(links[link] is not None and (links[link][0] == '2' or links[link][0] == '3') and 'birthtools.org' in link and '/files/' not in link):
					new_links = clean_page_links(get_page_links(link), base_url)
					links = merge_links(links, new_links)
		print(links)
	return links

results = check_links(all_links, base_url)

with open('results.json', 'w') as f:
	json.dump(results, f, sort_keys=True, indent = 2)


