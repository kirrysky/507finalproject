import unittest
import GetData as gd
import Database as db
import DataProcessing as dp
import sqlite3

DBNAME = 'hearthstone.db'

class TestStoreData(unittest.TestCase):

    def test_card_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT CardName FROM Cards'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Jade Idol',), result_list)
        self.assertEqual(len(result_list), 561)

        conn.close()

    def test_deck_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT DeckName
            FROM Decks
            WHERE HeroName="druid"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Chunchunner’s #15 Legend Spiteful Druid (April 2018)',), result_list)
        self.assertEqual(len(result_list), 1106)

        sql = '''
            SELECT COUNT(*)
            FROM Decks
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertEqual(count, 7935)

        conn.close()

    def test_composition_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT Sum(Count)
            FROM Compositions
            WHERE DeckName="Jade Druid Deck List Guide (Post Nerf) – Kobolds – April 2018"
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertEqual(count, 30)
        conn.close()

    def test_joins(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT Attack
            FROM Compositions
                JOIN Cards
                ON Compositions.CardId=Cards.Id
            WHERE Cards.CardName="Ironwood Golem"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(3, result_list[0][0])
        conn.close()

class TestProcessData(unittest.TestCase):
    def test_process_top_10_decks(self):
        self.assertEqual(len(dp.process_top_10_decks('druid')),10)
        self.assertEqual(dp.process_top_10_decks('druid')[1][1],583)
        self.assertEqual(dp.process_top_10_decks('druid')[2][0],'Midrange Fast Druid Deck List Guide – April 2016 (Season 25, Wild)')

    def test_process_crystal_usage(self):
        self.assertIn((1,2),dp.process_crystal_usage('Jade Druid Deck List Guide (Post Nerf) – Kobolds – April 2018','Class'))
        self.assertEqual(dp.process_crystal_usage('Jade Druid Deck List Guide (Post Nerf) – Kobolds – April 2018','Class')[1][1],2)

    def test_process_attack_or_health_usage(self):
        self.assertEqual(len(dp.process_attack_or_health_usage('Aggro Token Druid Deck List Guide (Post Nerf) – Kobolds – February 2018','Attack')),7)
        self.assertEqual(dp.process_attack_or_health_usage('Aggro Token Druid Deck List Guide (Post Nerf) – Kobolds – February 2018','Attack')[0][1],11)

        self.assertEqual(len(dp.process_attack_or_health_usage('Updated: Kolento’s KFT Midrange Bonemare Plague Druid','Health')),4)
        self.assertEqual(dp.process_attack_or_health_usage('Updated: Kolento’s KFT Midrange Bonemare Plague Druid','Health')[2][1],4)

    def test_process_race_composition(self):

        self.assertEqual(len(dp.process_race_composition('Jade Druid Deck List Guide (Post Nerf) – Kobolds – April 2018')),3)
        self.assertEqual(dp.process_race_composition('Jade Druid Deck List Guide (Post Nerf) – Kobolds – April 2018')[0][0],'Hero')
        self.assertEqual(dp.process_race_composition('Jade Druid Deck List Guide (Post Nerf) – Kobolds – April 2018')[1][1],9)

class TestGetData(unittest.TestCase):

    def test_get_data(self):
        results=gd.get_deck_data('druid')
        self.assertIsInstance(results,list)
        self.assertIsInstance(results[1],dict)
        self.assertIsInstance(gd.top_10_deck_components,dict)
        self.assertIsInstance(gd.all_cards_used,dict)

if __name__ == '__main__':
    unittest.main()
