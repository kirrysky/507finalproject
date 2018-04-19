#import requests
import json
from bs4 import BeautifulSoup
import requests

#Hearthstone heros
HEROS=['druid','hunter','mage','paladin','priest','rogue','shaman','warlock','warrior']
top_10_deck_components={}
all_cards_used={}
# on startup, try to load the cache from file
CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def make_request_using_cache(url):
    unique_ident = url
    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        #print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

def get_hero_data(heros):
    heros_dict={}
    for hero in heros:
        heros_dict[hero]=get_deck_data(hero)
    return heros_dict

def get_deck_data(hero):
    #### Execute funciton, get_umsi_data, here ####
    baseurl = 'http://www.hearthstonetopdecks.com/deck-category/deck-class/'
    hero_url=baseurl+hero+'/page/1'
    page_text = make_request_using_cache(hero_url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    #get pages
    pages = int(page_soup.find(class_="pages").text.split(" ")[-1])
    decks=[]
    for i in range(1,pages+1):
        baseurl = 'http://www.hearthstonetopdecks.com/deck-category/deck-class/'
        hero_url=baseurl+hero+'/page/'+str(i)
        page_text = make_request_using_cache(hero_url)
        page_soup = BeautifulSoup(page_text, 'html.parser')
        tbody = page_soup.find('tbody')
        trs=tbody.find_all('tr')
        for tr in trs:
            decks_dict={}
            tds=tr.find_all('td')
            deck_name=tds[1].find('h4').text
            deck_address=tds[1].find('h4').find('a')['href']
            deck_buildfee=int(tds[2].text.replace(',',''))
            deck_score=int(tds[4].text)
            decks_dict['deckname']=deck_name
            decks_dict['deckaddress']=deck_address
            decks_dict['deckbuildfee']=deck_buildfee
            decks_dict['deckscore']=deck_score
            decks.append(decks_dict)
    top_10_decks=sorted(decks,key=lambda x:x['deckscore'],reverse=True)[0:10]
    get_top_10_deck_component(hero,top_10_decks)
    #print(top_10_decks)
    return decks


def get_top_10_deck_component(hero,top_10_decks):
    global top_10_deck_components
    deck_compositions={}
    for each in top_10_decks:
        deck_url=each['deckaddress']
        page_text = make_request_using_cache(deck_url)
        page_soup = BeautifulSoup(page_text, 'html.parser')
        card_cols = page_soup.find_all(class_='col-md-12')
        cards_of_deck=[]
        for card_col in card_cols:
            if card_col.find('strong') is not None:
                card_kind=card_col.find('strong').text.split(" ")[0]
                cards=card_col.find_all('li')
                for each_card in cards:
                    card_cost=int(each_card.find(class_='card-cost').text)
                    card_address=each_card.find('a')['href']
                    get_card_information(card_address)
                    card_name=each_card.find(class_='card-name').text
                    card_count=int(each_card.find(class_='card-count').text)
                    card={}
                    card["kind"]=card_kind
                    card["cost"]=card_cost
                    card["name"]=card_name
                    card["count"]=card_count
                    card["address"]=card_address
                    cards_of_deck.append(card)
        deck_compositions[each['deckname']]=cards_of_deck
    top_10_deck_components[hero]=deck_compositions

def get_card_information(card_address):
    global all_cards_used
    page_text = make_request_using_cache(card_address)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    card=page_soup.find(class_='site-main')
    card_information={}
    card_name=card.find('h1').text
    card_more_info=card.find(class_='col-md-14')
    card_intro=card_more_info.find(class_='card-content').find('p').text
    card_li=card_more_info.find_all('li')
    if ('Type: Spell' in card_more_info.text) or ('Type: Hero' in card_more_info.text):
        #法术卡的处理
        mana_cost=card_li[0].text.split(' ')[-1]
        crafting_cost=card_li[1].text.split(':')[-1]
        if "Artist:" in card_more_info.text:
            rarity=card_li[4].text.split(' ')[-1]
            hero=card_li[5].find('a').text
            card_type=card_li[6].find('a').text
            season=card_li[7].find('a').text
        else:
            rarity=card_li[3].text.split(' ')[-1]
            hero=card_li[4].find('a').text
            card_type=card_li[5].find('a').text
            season=card_li[6].find('a').text
        card_information["mana_cost"]=int(mana_cost)
        card_information["crafting_cost"]=crafting_cost
        card_information["rarity"]=rarity
        card_information["hero"]=hero
        card_information["card_type"]=card_type
        card_information["season"]=season
    if ('Type: Minion' in card_more_info.text) or ('Type: Weapon' in card_more_info.text):
        #仆从卡的处理
        mana_cost=card_li[0].text.split(' ')[-1]
        attack=card_li[1].text.split(' ')[-1]
        health=card_li[2].text.split(' ')[-1]
        crafting_cost=card_li[3].text.split(':')[-1]
        if "Artist:" in card_more_info.text:
            rarity=card_li[6].text.split(' ')[-1]
            hero=card_li[7].find('a').text
            card_type=card_li[8].find('a').text
            if "Race:" in card_more_info.text:
                race=card_li[9].find('a').text
                season=card_li[10].find('a').text
            else:
                season=card_li[8].find('a').text
        else:
            rarity=card_li[5].text.split(' ')[-1]
            hero=card_li[6].find('a').text
            card_type=card_li[7].find('a').text
            if "Race:" in card_more_info.text:
                race=card_li[8].find('a').text
                season=card_li[9].find('a').text
                card_information["race"]=race
            else:
                season=card_li[8].find('a').text
        card_information["mana_cost"]=int(mana_cost)
        card_information["attack"]=int(attack)
        card_information["health"]=int(health)
        card_information["crafting_cost"]=crafting_cost
        card_information["rarity"]=rarity
        card_information["hero"]=hero
        card_information["card_type"]=card_type
        card_information["season"]=season
    card_information['intro']=card_intro
    all_cards_used[card_name]=card_information




def save_as_json(dict_name,file_name):
    dict_cache = json.dumps(dict_name,indent=4)
    f = open(file_name,"w")
    f.write(dict_cache)
    f.close()

hero_dictionary=get_hero_data(HEROS)
save_as_json(hero_dictionary,"hero_dictionary.json")
save_as_json(top_10_deck_components,"top_10_dictionary.json")
save_as_json(all_cards_used,"cards_dictionary.json")
