import sqlite3

class OperationalError(Exception):
	pass

def load(file, table, fields, query=-1, id=-1, query2=-1, id2=-1):
	db = sqlite3.connect(file)
	c = db.cursor()

	try:
		if query == -1 == id:
			c.execute(f"SELECT {fields} FROM {table}")
		elif query2 == -1 == id2:
			c.execute(f"SELECT {fields} FROM {table} WHERE {query}=?", (id,))
		else:
			c.execute(f"SELECT {fields} FROM {table} WHERE {query}=? AND {query2}=?", (id, id2))
	except(sqlite3.OperationalError):
		db.close()
		raise OperationalError

	m = c.fetchall()
	db.close()

	return m

def edit(file, table, field, newval, query, id, query2=-1, id2=-1):
	db = sqlite3.connect(file)
	c = db.cursor()

	try:
		if query2 == -1 == id2:
			c.execute(f"UPDATE {table} SET {field}=? WHERE {query}=?", (newval, id))
		else:
			c.execute(f"UPDATE {table} SET {field}=? WHERE {query}=? AND {query2}=?", (newval, id, id2))
	except(sqlite3.OperationalError):
		db.close()
		raise OperationalError

	db.commit()
	db.close()

def make_table(file, table, values):
	db = sqlite3.connect(file)
	c = db.cursor()

	try:
		c.execute(f"CREATE TABLE {table}({values})")
	except(sqlite3.OperationalError):
		db.close()
		raise OperationalError

	db.commit()
	db.close()

def drop_table(file, table):
	db = sqlite3.connect(file)
	c = db.cursor()

	try:
		c.execute(f"DROP TABLE {table}")
	except(sqlite3.OperationalError):
		db.close()
		raise OperationalError

	db.commit()
	db.close()

def insert(file, table, fields, newvals):
	db = sqlite3.connect(file)
	c = db.cursor()

	count = 0
	for i in fields:
		if i == ",":
			count += 1
	values = "?, " * count + "?"

	try:
		c.execute(f"INSERT INTO {table}({fields}) VALUES({values})", (newvals))
	except(sqlite3.OperationalError):
		db.close()
		raise OperationalError

	db.commit()
	db.close()

def delete(file, table, query, id):
	db = sqlite3.connect(file)
	c = db.cursor()

	try:
		c.execute(f"DELETE FROM {table} WHERE {query}=?", (id,))
	except(sqlite3.OperationalError):
		db.close()
		raise OperationalError

	db.commit()
	db.close()

def get_all(file, table, val):
	db = sqlite3.connect(file)
	cursor = db.cursor()

	try:
		cursor.execute(f"SELECT {val} FROM {table}")
	except(sqlite3.OperationalError):
		db.close()
		raise OperationalError

	h = cursor.fetchall()
	m = []

	for i in h:
		m.append(i[0])

	db.close()
	return m

def get_tables(file):
	db = sqlite3.connect(file)
	cursor = db.cursor()
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	h = cursor.fetchall()
	m = []

	for i in h:
		m.append(i[0])

	db.close()
	return m

def rename_table(file, table, name):
	db = sqlite3.connect(file)
	cursor = db.cursor()

	try:
		cursor.execute(f"ALTER TABLE {table} RENAME TO {name}")
	except(sqlite3.OperationalError):
		db.close()
		raise OperationalError

	db.commit()
	db.close()

def clear(file, table, column):
	db = sqlite3.connect(file)
	cursor = db.cursor()

	try:
		cursor.execute(f"DELETE FROM {table} WHERE {column}={column}")
	except(sqlite3.OperationalError):
		db.close()
		raise OperationalError