
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
    StudentId INTEGER REFERENCES mathematicians (Id),
    PRIMARY KEY (
        AdviserId,
        StudentId
    ) ON CONFLICT IGNORE
);
"""

import sqlite3 as db

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

