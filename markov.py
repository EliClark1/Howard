import sqlite3
from random import choice, randint

def create(db, word=-1, count=30):
	if word == -1:
		m = get_keys(db)
		word = choice(m)
	m = word

	for i in range(count):
		try:
			data = read(db, word)
			h = randint(0, len(data)-1)
			word = data[h][0]
			m += " " + str(word)
		except(ValueError):
			try:
				data = read(db, word)
				h = randint(0, len(data)-1)
				word = data[h][0]
				m += " " + str(word)
			except(ValueError):
				pass
			except(IndexError):
				pass
		except(IndexError):
			pass
	return m

def read(file, key):
    db = sqlite3.connect(file)
    cursor = db.cursor()
    cursor.execute("SELECT value FROM markov WHERE key=?", (key,))

    m = cursor.fetchall()
    db.close()

    return m
	
def write(file, text):
    db = sqlite3.connect(file)
    cursor = db.cursor()

    try:
        text = text.split()
    except(AttributeError):
        pass

    for i in range(len(text)):
        try:
            cursor.execute("INSERT INTO markov (key, value) VALUES (?, ?)",
                (text[i], text[i+1]))
        except(IndexError):
            cursor.execute("INSERT INTO markov (key, value) VALUES (?, ?)",
                (text[i], ""))

    db.commit()
    db.close()

def get_keys(file):
    db = sqlite3.connect(file)
    cursor = db.cursor()
    cursor.execute("SELECT key FROM markov")
    h = cursor.fetchall()
    m = []
    for i in h:
        m.append(i[0])

    db.close()
    return m
