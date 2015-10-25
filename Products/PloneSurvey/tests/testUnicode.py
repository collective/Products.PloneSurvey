# coding: utf8

import unittest

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from base import INTEGRATION_TESTING
from base import fixLineEndings


class TestUnicodeInSpreadsheet(unittest.TestCase):
    """Ensure unicode does not break csv"""
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Survey', 's1')
        self.s1 = getattr(self.portal, 's1')

    def testUnicodeInTextAnswer(self):
        s1 = getattr(self, 's1')
        s1.invokeFactory('Survey Text Question', 'stq1')
        stq1 = getattr(s1, 'stq1')
        stq1.addAnswer(u'あいうえお')
        csv_file = s1.buildSpreadsheet2()
        csv_list = fixLineEndings(csv_file)
        csv_list = csv_list.split("\n")
        # this is a hiragana a utf8 encoded
        assert '\xe3\x81\x82' == csv_list[1][16:19], "Answer not in file"
        assert len(csv_list[1].split(',')) == 3, "Answer treated as list"

    def testUnicodeInSelectAnswer(self):
        s1 = getattr(self, 's1')
        s1.invokeFactory('Survey Select Question', 'ssq1')
        ssq1 = getattr(s1, 'ssq1')
        ssq1.setInputType('radio')
        ssq1.addAnswer(u'あいうえお')
        csv_file = s1.buildSpreadsheet2()
        csv_list = fixLineEndings(csv_file)
        csv_list = csv_list.split("\n")
        # this is a hiragana a utf8 encoded
        assert '\xe3\x81\x82' == csv_list[1][16:19], "Answer not in file"
        assert len(csv_list[1].split(',')) == 3, "Answer treated as list"
