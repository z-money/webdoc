from lxml import html

import requests
import time
import sys

class link_checker:
	def __init__(self, base_url, delay = 0):
		self.base_url = base_url

		# detect the protocol (assume http)
		if(base_url.startswith('https')):
			self.protocol = 'https'
		else:
			self.protocol = 'http'

		# strip the protocol from the domain
		domain = base_url.strip('http://')
		domain = base_url.strip('https://')
		domain = base_url.strip('www.')

		# the domain
		self.domain = domain
		
		# initialize some empty arrays
		# checked links is a list of all links we have looked at
		self.checked_links = []
		# list of any link that didn't return a 200
		self.bad_links = []

		# delay in seconds between checking links
		self.delay = float(delay)

	def is_relative(self, url):
		if('www.' in url or 'http://' in url or 'https://' in url):
			return False
		else:
			return True

	def get_links(self, url):
		if(url.startswith('//')):
			url = self.protocol + ':' + url
		page = requests.get(url)
		tree = html.fromstring(page.content)

		# hey, look! We're using XPath!
		# this just looks for anchor tags with an href in them
		# this doesn't neccesarrily capture all links (e.g img links)
		# but it captures what we're interested in for this project
		# could be updated to be more modular
		links = tree.xpath('//a/@href')

		return links

	def check_site(self, url, follow_domain_links = True):
		self.checked_links.append(url)
		self.check_link(url)

		links = self.get_links(url)
		for link in links:
			if(link in self.checked_links or link.startswith('#')):
				continue

			self.checked_links.append(link)
			# print('checked '+str(len(self.checked_links))+' links')

			if(link.startswith('//')):
				link = self.protocol + ':' + link

			if(self.is_relative(link) and follow_domain_links == True):
				link = link.strip('/')
				self.check_site(self.domain + '/' + link)
			elif(self.domain in link and follow_domain_links == True):
				self.check_site(link)
			elif(self.is_relative(link)):
				link = link.strip('/')
				self.check_link(self.domain + '/' + link, url)
			else:
				self.check_link(link, url)

			# optional delay to avoid overloading the server/looking malicious
			if(self.delay > 0):
				time.sleep(self.delay)

	def check_link(self, url, page_url = None):
		try:
			page = requests.get(url, allow_redirects=False)
			if(page.status_code != 200):
				# if we don't get a 200 this is considered a bad link
				self.bad_links.append({'link':url, 'status_code':page.status_code, 'page':page_url})
			return page.status_code
		except Exception as e:
			self.bad_links.append({'link':url, 'status_code':-1, 'page':page_url, 'error_message':str(e)})
			return -1