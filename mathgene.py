
from collections import defaultdict

import urllib2
import xml.etree.ElementTree as ET

#from HTMLParser import HTMLParser


#tree = ET.parse('country_data.xml')
#root = tree.getroot()
import bs4


def fix_whitespace(string):
	return ' '.join(string.split())

class data: pass

KYLE = 188052
EMILIO = 114748


if __name__ == '__main__':
	math_url_template = 'https://genealogy.math.ndsu.nodak.edu/id.php?id=%d'
	math_id = 114748
	download_not_load = False
	to_file = 'Emilio.html'

	def download_math():
		me_url = math_url_template % math_id
		f = urllib2.urlopen(me_url)
		return f.read()

	def id_from_math_link(link_str):
		return int( link_str.split('=')[-1] )

	def person_from_anchor(anchor):
		return dict(name=anchor.string,
			id=id_from_math_link(anchor['href'])
			)

	math_html = None
	if download_not_load:
		math_html = download_math()
		with open(to_file,'w') as f: f.write(math_html)

	else:
		with open(to_file,'r') as f:
			math_html = f.read()

	def get_soup(math_html):
		return bs4.BeautifulSoup(math_html)

	def get_math(math_html):
		_w = fix_whitespace

		# need to get my OWN ID!

		soup = get_soup(math_html)
		
		main = soup.find(id='mainContent')

		name = fix_whitespace(main.h2.string)
		#.strip()

		degree_data = main.span.contents

		degree = degree_data[0]
		degree_year = int(degree_data[-1])

		degree_inst = degree_data[1].string
		location = main.img.attrs['title']

		thesis = main.find(id='thesisTitle').string

		# advisors
		advisors_tag = main.img.find_next('a').parent
		advisors = advisors_tag.find_all('a')

		advisors = [
			person_from_anchor(a)
			for a in advisors
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
			location = _w(location),
			year = degree_year,
			thesis = _w(thesis),
			advisors = advisors,
			students = students
			)

	person = get_math(math_html)
	print person





