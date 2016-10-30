CREATE TABLE mathematicians IF NOT EXISTS (
    Id          INTEGER PRIMARY KEY,
    Name        TEXT,
    Degree      TEXT,
    Institution TEXT,
    Country     TEXT,
    Year        INTEGER,
    Thesis      TEXT
);

CREATE TABLE adviserships (
    AdviserId INTEGER REFERENCES mathematicians (Id),
    StudentId INTEGER REFERENCES mathematicians (Id),
    PRIMARY KEY (
        AdviserId,
        StudentId
    )
);
