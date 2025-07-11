### CREATING TABLES
create_full_trans = \
"""
CREATE TABLE IF NOT EXISTS full_trans (
    full_id INTEGER PRIMARY KEY AUTOINCREMENT,
    interviewee_id INTEGER,
    language VARCHAR(2),
    start TIMESTAMPZ,
    end TIMESTAMPZ,
    full_script TEXT,
    platform VARCHAR(12)
);
"""

create_part_trans = \
"""
CREATE TABLE IF NOT EXISTS part_trans (
    part_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_id INTEGER,
    start TIMESTAMPZ,
    end TIMESTAMPZ, 
    script TEXT
);
"""

### INSERT INTO TABLES
insert_many_part_trans = "INSERT INTO part_trans VALUES (?,?,?,?)"
insert_many_full_trans = "INSERT INTO full_trans " \
    "(interviewee_id, language, start, end, full_script, platform)" \
    "VALUES (?,?,?,?,?,?)"

### DROP TABLES
drop_table_format = "DROP TABLE {table};"
drop_part_trans = "DROP TABLE full_trans;"
drop_full_trans = "DROP TABLE full_trans;"