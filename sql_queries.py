CREATE_TABLE_CAR = """
CREATE TABLE IF NOT EXISTS car (
    id INTEGER PRIMARY KEY,
    color TEXT,
    type TEXT,
    model TEXT
);
"""

INSERT_CAR = """
INSERT OR REPLACE INTO car (id, color, type, model)
VALUES ({id}, '{color}', '{type}', '{model}');
"""

CREATE_TABLE_USER = """
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
);
"""

INSERT_USER = """
INSERT OR REPLACE INTO user (id, name, age)
VALUES ({id}, '{name}', {age});
"""
