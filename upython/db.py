import btree

def write(key, value):
    try:
        f = open('system.db', 'r+b')
    except OSError:
        f = open('system.db', 'w+b')
    db = btree.open(f)
    db[key] = value
    db.flush()
    assert key in db
    assert db[key] == value
    db.close()
    f.close()

def read(key):
    try:
        f = open('system.db', 'r+b')
    except OSError:
        f = open('system.db', 'w+b')
    db = btree.open(f)
    try:
        value = db[key]
    except:
        value = b'-1'
    db.close()
    f.close()
    return value

def delete(key):
    try:
        f = open('system.db', 'r+b')
    except OSError:
        f = open('system.db', 'w+b')
    db = btree.open(f)
    res = 0
    try:
        del db[key]
    except:
        res = -1
    assert not key in db
    db.close()
    f.close()
    return res
