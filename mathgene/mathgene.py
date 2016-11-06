#from collections import defaultdict

import urllib2
#import xml.etree.ElementTree as ET
import bs4


def fix_whitespace(string):
	return ' '.join(string.split())

class data: pass




def id_from_mathematician_link(link_str):
	return int( link_str.split('=')[-1] )

def person_from_anchor(anchor):
	return dict( name=anchor.string, id=id_from_mathematician_link(anchor['href']) )

def download_mathematician_html(id):
	URL_TEMPLATE = 'https://genealogy.math.ndsu.nodak.edu/id.php?id=%d'
	return urllib2.urlopen(URL_TEMPLATE % id).read()

def scrape_mathematician(math_html):
	_w = fix_whitespace

	soup = bs4.BeautifulSoup(math_html)

	main = soup.find(id='mainContent')

	# name
	name = _w(main.h2.string)
	
	# degree
	degree_data = main.span.contents

	degree = degree_data[0]
	degree_year = int(degree_data[-1])
	degree_inst = degree_data[1].string
	degree_loc = main.img.attrs['title']

	# thesis
	thesis = main.find(id='thesisTitle').string

	# advisers
	advisers_tag = main.img.find_next('a').parent
	advisers = advisers_tag.find_all('a')

	advisers = [
		person_from_anchor(a)
		for a in advisers
		]

	# students
	students = main.table
	if students is None:
		students = []

	else:
		students = main.table.find_all('tr')[1:]
		students = [
			person_from_anchor(tag.a)
			for tag in students
			]

	return dict(
		name = _w(name),
		degree = _w(degree),
		institution = _w(degree_inst),
		location = _w(degree_loc),
		year = degree_year,
		thesis = _w(thesis),
		advisers = advisers,
		students = students
		)

def download_mathematician(id):
	math_html = download_mathematician_html(id)
	person = scrape_mathematician(math_html)
	person.update(id=id)
	return person




KYLE = 188052
EMILIO = 114748

if __name__ == '__main__':
	#import pickle
	import json

	import argparse
	parser = argparse.ArgumentParser()
	#parser.add_argument('--reset',type=bool,action='store_true')
	parser.add_argument('id', type=int)
	parser.add_argument('filename', type=str)

	args = parser.parse_args()
	
	person = download_mathematician(args.id)

	with open(args.filename,'w') as f:
		json.dump(person,f)
	#with open(args.filename,'w') as f:
	#pickle.dump(person,f)



	"""
	math_id = 114748
	download_not_load = False
	to_file = 'Emilio.html'

	math_html = None
	if download_not_load:
		math_html = download_math()
		with open(to_file,'w') as f: f.write(math_html)

	else:
		with open(to_file,'r') as f:
			math_html = f.read()

	def get_math(math_html):
		_w = fix_whitespace

		# need to get my OWN ID!

		soup = get_soup(math_html)
		

	person = get_math(math_html)
	print person
	"""




