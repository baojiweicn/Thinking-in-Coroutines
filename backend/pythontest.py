#!/usr/bin/env python
# encoding: utf-8
import unittest
import impl

class PythonTest(unittest.TestCase):

    def test_table_to_dict_list(self):
        table = [
            ['Month', 'Day', 'ItemName', 'NumberofItems', 'Price', 'RetailPrice', 'Tax', 'Code', 'SupplierName'],
            ['01', '01', 'Corporate Creditcard Usage', '', '', '10,364', '1,036', '00140', 'KoreaMcDGangnam'],
            ['01', '01', 'Corporate Creditcard Usage', '', '', '10,999', '1,101', '00406', 'SpicyChickenBundang'],
            ['01', '01', 'Corporate Creditcard Usage', '', '', '1,818', '182', '00237', 'PorkBBQItaewon']
        ]

        dict_list = impl.table_to_dict_list(table)
        self.assertEqual('10,364', dict_list[0]['RetailPrice'])
        self.assertEqual('PorkBBQItaewon', dict_list[1]['SupplierName'])
        #Unittest result is not correct 

    def test_filter_list(self):
        data = range(0, 100)

        filtered = impl.multiple_of_three(data)

        for number in filtered:
            self.assertTrue(number % 3 == 0)

    def test_json(self):
        data = '''{
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}'''

        self.assertEqual('Standard Generalized Markup Language', impl.pick_GlossTerm(data))

    def test_sorted_distinct_list(self):
        data = [1, 5, 8, 10, 4, 9, 11, 10, 8, 14, 3, 4]

        self.assertEqual([1, 3, 4, 5, 8, 9, 10, 11, 14], impl.sort_and_distinct(data))

    def test_custom_sort(self):
        class Voucher:
            def __init__(self, trader, amount):
                self.trader = trader
                self.amount = amount


        data = [
            Voucher('GSMart', 125000),
            Voucher('7 Eleven', 8500),
            Voucher('Shinsegae', 288000),
            Voucher('Emart', 80000),
        ]

        vouchers = impl.sort_by_amount(data)
        self.assertEqual('Shinsegae', vouchers[0].trader)
        self.assertEqual('7 Eleven', vouchers[-1].trader)

    def test_dispatch_by_string(self):
        self.assertEqual(18, impl.calc('multiply', 6, 3))
        self.assertEqual(2, impl.calc('divide', 6, 3))
        self.assertEqual(9, impl.calc('add', 6, 3))
        self.assertEqual(3, impl.calc('subtract', 6, 3))

    def test_traverse(self):
        unix_tree = {
            'Unix': {
                'PWB/Unix': {
                    'System III': {
                        'HP-UX': None
                    },
                    'System V': {
                        'UnixWare': None,
                        'Solaris': {
                            'OpenSolaris': None
                        }
                    }
                },
                'BSD': {
                    'Unix 9': None,
                    'FreeBSD': None,
                    'NetBSD': None,
                    'MacOS': None
                },
                'Xenix': {
                    'Sco Unix': {
                        'OpenServer': None
                    },
                    'AIX': None,
                },
            },
            'Linux': {
                'Debian': {
                    'Ubuntu': None,
                    'Linux Mint': None
                },
                'Redhat': {
                    'CentOS': None,
                    'Fedora': None
                },
                'Gentoo': None
            }
        }

        self.assertEqual('OpenSolaris', impl.find_deepest_child(unix_tree))
        self.assertSetEqual({'Unix', 'BSD', 'Linux'}, impl.find_nodes_that_contains_more_than_three_children(unix_tree))
        self.assertEqual(7, impl.count_of_all_distributions_of_linux(unix_tree))

    def test_polymorphism(self):
        messages = [
            impl.Notice('Welcome to chat'),
            impl.Message(userid=1, content='Hello World'),
            impl.Message(userid=2, content='Lorem ipsum dolor sit amet, consectetur adipiscing elit.'),
            impl.Message(userid=3, content='안녕하세요.'),
            impl.Message(userid=2, content='ありがとうございます。'),
        ]

        self.assertEqual('''<li class="notice">Welcome to chat</li>
<li class="left">
    <img class="profile" src="${user_image(1)}">
    <div class="message-content">Hello World</div>
</li>
<li class="right">
    <img class="profile" src="${user_image(2)}">
    <div class="message-content">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>
</li>
<li class="left">
    <img class="profile" src="${user_image(3)}">
    <div class="message-content">안녕하세요.</div>
</li>
<li class="right">
    <img class="profile" src="${user_image(2)}">
    <div class="message-content">ありがとうございます。</div>
</li>''', impl.render_messages(messages, current_userid=2))
