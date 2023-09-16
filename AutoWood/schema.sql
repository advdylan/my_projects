CREATE TABLE furnitures (
    id INTEGER INDENTITY,
    EAN INTEGER PRIMARY KEY,
    type TEXT,
    model TEXT ,
    color TEXT,
    wood TEXT,
    size TEXT
);
CREATE TABLE warehouse (
    id INTEGER INDENTITY,
    EAN_CODE INTEGER,
    date TEXT,
    FOREIGN KEY (EAN_CODE) REFERENCES furnitures(EAN)
);

