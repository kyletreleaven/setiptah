
SCHEMA = """
CREATE TABLE %(mathematicians)s (
    Id          INTEGER PRIMARY KEY,
    Name        TEXT,
    Degree      TEXT,
    Institution TEXT,
    Country     TEXT,
    Year        INTEGER,
    Thesis      TEXT
);

CREATE TABLE %(adviserships)s (
    AdviserId INTEGER REFERENCES mathematicians (Id),
    AdviserName TEXT,
    StudentId INTEGER REFERENCES mathematicians (Id),
    StudentName TEXT,
    PRIMARY KEY (
        AdviserId,
        StudentId
    ) ON CONFLICT IGNORE
);
"""

import sqlite3 as db

class MathgeneCursor:
	def __init__(self, cursor):
		self._c = cursor

	def fetch_advisers(self, id):
		self._c.execute('SELECT AdviserId,AdviserName FROM adviserships WHERE StudentId=?', (id,) )
		return [ dict( zip(['id','name'], tup) ) for tup in self._c.fetchall() ]

	def fetch_students(self, id):
		self._c.execute('SELECT StudentId,StudentName FROM adviserships WHERE AdviserId=?', (id,) )
		return [ dict( zip(['id','name'], tup) ) for tup in self._c.fetchall() ]

	def fetch_math_record(self, id):
		self._c.execute('SELECT * FROM mathematicians WHERE Id=?', (id,) )
		row = self._c.fetchone()

		if row is not None:
			row = self.record_form(row)

		return row

	def fetch_mathematician(self, id):
		rec = self.fetch_math_record(id)

		if rec is not None:
			# then, add advisers
			rec['advisers'] = self.fetch_advisers(id)

			# and students!
			rec['students'] = self.fetch_students(id)

		return rec

	def insert_math_record(self, rec):
		tup = self.tuple_form(rec)
		self._c.execute('INSERT INTO mathematicians VALUES (?,?,?,?,?,?,?)', tup )

	def insert_advisers(self, id, advisers):
		adviser_edges = [ (a['id'], a['name'], id, None) for a in advisers ]
		#print adviser_edges
		self._c.executemany('INSERT INTO adviserships VALUES (?,?,?,?)', adviser_edges)

	def insert_students(self, id, students):
		student_edges = [ (id, None, s['id'], s['name']) for s in students ]
		#print adviser_edges
		self._c.executemany('INSERT INTO adviserships VALUES (?,?,?,?)', student_edges)

	def insert_mathematician(self, rec):
		self.insert_math_record(rec)
		self.insert_advisers(rec['id'], rec['advisers'])
		self.insert_students(rec['id'], rec['students'])

	@staticmethod
	def tuple_form(rec):
		return (rec['id'], rec['name'], rec['degree'], rec['institution'], 
					rec['location'], rec['year'], rec['thesis'])

	@staticmethod
	def record_form(tup):
		KEY_ORDER = ['id', 'name', 'degree', 'institution', 'location', 'year', 'thesis']
		return dict(zip(KEY_ORDER, tup))


def createdb(filename, **kwargs):
	conn = db.connect(filename)
	c = conn.cursor()

	kwargs.setdefault('mathematicians','mathematicians')
	kwargs.setdefault('adviserships','adviserships')

	c.executescript(SCHEMA % kwargs)

	conn.commit()
	conn.close()




if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	#parser.add_argument('--reset',type=bool,action='store_true')

	parser.add_argument('filename', type=str)
	args = parser.parse_args()

	createdb(args.filename)

