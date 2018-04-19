import sqlite3
import json

#datebase name
DBNAME = 'hearthstone.db'

#some data which should included
HEROS=['druid','hunter','mage','paladin','priest','rogue','shaman','warlock','warrior','neutral']
HEROSJSON = 'hero_dictionary.json'
TOP10JSON = 'top_10_dictionary.json'
CARDSJSON = 'cards_dictionary.json'

def create_db():
    #first step create a database
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    #first table:heros
    statement = '''
        DROP TABLE IF EXISTS 'Heros';
    '''
    cur.execute(statement)

    statement = '''
            CREATE TABLE IF NOT EXISTS 'Heros' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'HeroName' TEXT
            );
        '''
    cur.execute(statement)

    #second table:decks
    statement = '''
        DROP TABLE IF EXISTS 'Decks';
    '''
    cur.execute(statement)

    statement = '''
            CREATE TABLE IF NOT EXISTS 'Decks' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'DeckName' TEXT,
                'DeckAddress' TEXT,
                'DeckBuildFee' INTEGER,
                'DeckScore' INTEGER,
                'HeroName' TEXT,
                'HeroId' INTEGER,
                FOREIGN KEY('HeroId') REFERENCES Heros(Id)
            );
        '''
    cur.execute(statement)

    #third table:cards
    statement = '''
        DROP TABLE IF EXISTS 'Cards';
    '''
    cur.execute(statement)

    statement = '''
            CREATE TABLE IF NOT EXISTS 'Cards' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'CardName' TEXT,
                'ManaCost' INTEGER,
                'CraftingCost' TEXT,
                'Rarity' TEXT,
                'HeroName' TEXT,
                'HeroId' INTEGER,
                'Type' TEXT,
                'Season' TEXT,
                'Intro' TEXT,
                'Race' TEXT,
                'Attack' INTEGER,
                'Health' INTEGER,
                FOREIGN KEY('HeroId') REFERENCES Heros(Id)
            );
        '''
    cur.execute(statement)

    #third table:cards
    statement = '''
        DROP TABLE IF EXISTS 'Compositions';
    '''
    cur.execute(statement)

    statement = '''
            CREATE TABLE IF NOT EXISTS 'Compositions' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'DeckName' TEXT,
                'DeckId' INTEGER,
                'CardName' TEXT,
                'CardId' INTEGER,
                'HeroName' TEXT,
                'HeroId' INTEGER,
                'Kind' TEXT,
                'CardAddress' TEXT,
                'Count' INTEGER,
                FOREIGN KEY('DeckId') REFERENCES Decks(Id),
                FOREIGN KEY('CardId') REFERENCES Cards(Id),
                FOREIGN KEY('HeroId') REFERENCES Heros(Id)
            );
        '''

    cur.execute(statement)

    conn.commit()
    conn.close()


def insert_heros():

    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    for each in HEROS:
        insertion = (each,)
        statement = 'INSERT INTO "Heros" (HeroName)'
        statement += 'VALUES (?)'
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()

def insert_decks():

    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    try:
        cache_file = open(HEROSJSON, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()

    # if there was no file, no worries. There will be soon!
    except:
        CACHE_DICTION = {}

    for each in CACHE_DICTION:
        hero_name=each
        for deck in CACHE_DICTION[each]:
            deck_name=deck['deckname']
            deck_address=deck['deckaddress']
            deck_build_fee=deck['deckbuildfee']
            deck_score=deck['deckscore']
            insertion = (deck_name,deck_address,deck_build_fee,deck_score,hero_name,hero_name)
            statement = 'INSERT INTO "Decks" (DeckName,DeckAddress,DeckBuildFee,DeckScore,HeroName,HeroId)'
            statement += 'VALUES (?, ?, ?, ?, ?, (SELECT id From Heros WHERE HeroName=?))'
            cur.execute(statement, insertion)

    conn.commit()
    conn.close()

def insert_cards():

    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    try:
        cache_file = open(CARDSJSON, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()

    # if there was no file, no worries. There will be soon!
    except:
        CACHE_DICTION = {}

    for each in CACHE_DICTION:
        card_name=each
        card=CACHE_DICTION[each]
        mana_cost=card['mana_cost']
        crafting_cost=card['crafting_cost']
        rarity=card['rarity']
        hero=card['hero'].lower()
        card_type=card['card_type']
        season=card['season']
        intro=card['intro']
        if card.__contains__('race'):
            race=card['race']
        else:
            race=None
        if card.__contains__('attack'):
            attack=card['attack']
            health=card['health']
            insertion = (card_name,mana_cost,crafting_cost,rarity,hero,hero,card_type,season,intro,race,attack,health)
            statement = 'INSERT INTO "Cards" (CardName,ManaCost,CraftingCost,Rarity,HeroName,HeroId,Type,Season,Intro,Race,Attack,Health)'
            statement += 'VALUES (?, ?, ?, ?, ?,(SELECT id From Heros WHERE HeroName=?),?,?,?,?,?,?)'
        else:
            insertion = (card_name,mana_cost,crafting_cost,rarity,hero,hero,card_type,season,intro,race)
            statement = 'INSERT INTO "Cards" (CardName,ManaCost,CraftingCost,Rarity,HeroName,HeroId,Type,Season,Intro,Race)'
            statement += 'VALUES (?, ?, ?, ?, ?, (SELECT id From Heros WHERE HeroName=?),?,?,?,?)'
        cur.execute(statement, insertion)


    conn.commit()
    conn.close()

def insert_compositions():

    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print(e)

    try:
        cache_file = open(TOP10JSON, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()

    # if there was no file, no worries. There will be soon!
    except:
        CACHE_DICTION = {}

    for each in CACHE_DICTION:
        hero_name=each
        for deck_name in CACHE_DICTION[each]:
            for card in CACHE_DICTION[each][deck_name]:
                card_name=card["name"]
                card_kind=card["kind"]
                card_address=card["address"]
                card_count=card["count"]
                insertion = (deck_name,deck_name,card_name,card_name,hero_name,hero_name,card_kind,card_address,card_count)
                statement = 'INSERT INTO "Compositions" (DeckName,DeckId,CardName,CardId,HeroName,HeroId,Kind,CardAddress,Count)'
                statement += 'VALUES (?, (SELECT id From Decks WHERE DeckName=?), ?, (SELECT id From Cards WHERE CardName=?), ?, (SELECT id From Heros WHERE HeroName=?),?,?,?)'
                cur.execute(statement, insertion)

    conn.commit()
    conn.close()

# Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    create_db()
    insert_heros()
    insert_decks()
    insert_cards()
    insert_compositions()
