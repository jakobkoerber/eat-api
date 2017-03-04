# -*- coding: utf-8 -*-

import unittest

from lxml import html
from datetime import date
from menu_parser import StudentenwerkMenuParser
from entities import Dish, Menu, Week
import json


class StudentenwerkMenuParserTest(unittest.TestCase):
    studentenwerk_menu_parser = StudentenwerkMenuParser()

    menu_html = html.fromstring(open("src/test/assets/speiseplan_garching.htm").read())
    menu_html_wrong_date_format = html.fromstring(
        open("src/test/assets/speiseplan_garching_wrong_date_format.htm").read())

    dish1_1 = Dish("Linseneintopf mit Gemüse (v)", 1)
    dish1_2 = Dish("Pfannkuchen mit Apfelmus (f) (3)", 1.55)
    dish1_3 = Dish("Fischstäbchen (MSC) mit Remouladensauce (1,2,3,9)", 1.9)
    dish1_4 = Dish("Linseneintopf mit ein Paar Wiener (R,S) (2,3,8)", 1.9)

    dish2_1 = Dish("Polenta mit Pilzen und Zwiebeln (v)", 1)
    dish2_2 = Dish("Gnocchi mit Schafskäse und frischem Basilikum (f)", 1.9)
    dish2_3 = Dish("Rinderroulade nach Hausfrauenart mit Senf-Gemüse-Sauce (R,S) (2,3,99)", 2.6)
    dish2_4 = Dish("Smoky Mountain Chicken (mit Käse und Vorderschinken überb.) (1,2,3,8,10,11)", 2.8)

    menu1_date = date(2016, 12, 23)
    menu2_date = date(2017, 1, 11)

    menu1 = Menu(menu1_date, [dish1_1, dish1_2, dish1_3, dish1_4])
    menu2 = Menu(menu2_date, [dish2_1, dish2_2, dish2_3, dish2_4])

    def test_should_return_menu(self):
        self.assertEqual(self.menu1, self.studentenwerk_menu_parser.get_menus(self.menu_html)[self.menu1_date])
        self.assertEqual(self.menu2, self.studentenwerk_menu_parser.get_menus(self.menu_html)[self.menu2_date])

    def test_should_return_none(self):
        self.assertEqual(18, len(self.studentenwerk_menu_parser.get_menus(self.menu_html_wrong_date_format)))

    def test_should_return_json(self):
        with open('src/test/assets/speiseplan_garching_kw2016-51.json') as data_file:
            week_2016_51 = json.load(data_file)
        with open('src/test/assets/speiseplan_garching_kw2016-51.json') as data_file:
            week_2017_02 = json.load(data_file)
        with open('src/test/assets/speiseplan_garching_kw2016-51.json') as data_file:
            week_2017_03 = json.load(data_file)
        with open('src/test/assets/speiseplan_garching_kw2016-51.json') as data_file:
            week_2017_04 = json.load(data_file)

        menus = self.studentenwerk_menu_parser.get_menus(self.menu_html)
        weeks = Week.to_weeks(menus)
        week_2016_51_actual = json.loads(weeks[51].to_json())
        week_2017_02_actual = json.loads(weeks[2].to_json())
        week_2017_03_actual = json.loads(weeks[3].to_json())
        week_2017_04_actual = json.loads(weeks[4].to_json())

        self.assertEqual(sorted(week_2016_51_actual.items()), sorted(week_2016_51.items()))
        # TODO add correct prices to test json
        # self.assertEqual(sorted(week_2017_02_actual.items()), sorted(week_2017_02.items()))
        # self.assertEqual(sorted(week_2017_03_actual.items()), sorted(week_2017_03.items()))
        # self.assertEqual(sorted(week_2017_04_actual.items()), sorted(week_2017_04.items()))

    def test_should_return_weeks(self):
        menus = self.studentenwerk_menu_parser.get_menus(self.menu_html)
        weeks_actual = Week.to_weeks(menus)

        self.assertEqual(4, len(weeks_actual))
        for calendar_week in weeks_actual:
            week = weeks_actual[calendar_week]
            self.assertEqual(5, len(week.days))
