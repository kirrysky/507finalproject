import sqlite3
import csv
import json

DBNAME = 'hearthstone.db'
HEROS=['druid','hunter','mage','paladin','priest','rogue','shaman','warlock','warrior']

#the first process
def process_top_10_decks(hero_name):
    results=[]
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    statement = 'SELECT DeckName,DeckScore '
    statement += 'FROM Decks '
    statement += 'WHERE HeroName=? '
    statement += 'ORDER BY DeckScore '
    statement += 'DESC '
    statement += 'LIMIT 10 '

    param=(hero_name,)
    cur.execute(statement, param)
    for row in cur:
        results.append(row)

    conn.commit()
    conn.close()

    return results

#the second process
def process_crystal_usage(deck_name,kind):
    results=[]
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    statement = 'SELECT ManaCost,Count(*) '
    statement += 'FROM Compositions '
    statement += 'JOIN Cards '
    statement += 'On Compositions.CardId=Cards.Id '
    statement += 'WHERE DeckName=? AND Kind=?'
    statement += 'GROUP BY ManaCost '

    param=(deck_name,kind)
    cur.execute(statement, param)

    for row in cur:
        print (row)
        results.append(row)

    conn.commit()
    conn.close()

    return results

def process_attack_or_health_usage(deck_name,ability):
    results=[]
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    if ability=='Attack':
        statement = 'SELECT Attack,sum(Count) '
    elif ability=='Health':
        statement = 'SELECT Health,sum(Count) '
    statement += 'FROM Compositions '
    statement += 'JOIN Cards '
    statement += 'On Compositions.CardId=Cards.Id '
    statement += 'WHERE DeckName=? '
    if ability=='Attack':
        statement += 'GROUP BY Attack '
    elif ability=='Health':
        statement += "AND Type='Minion' "
        statement += 'GROUP BY Health '

    param=(deck_name,)
    cur.execute(statement, param)

    for row in cur:
        results.append(row)

    conn.commit()
    conn.close()
    return results

def process_race_composition(deck_name):
    results=[]
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    statement = 'SELECT Type,sum(Count) '
    statement += 'FROM Compositions '
    statement += 'JOIN Cards '
    statement += 'On Compositions.CardId=Cards.Id '
    statement += 'WHERE DeckName=? '
    statement += 'GROUP BY Type '

    param=(deck_name,)
    cur.execute(statement, param)

    for row in cur:
        results.append(row)

    conn.commit()
    conn.close()
    return results
