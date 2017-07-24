import unittest

from wifidb.settings import OUI_FILE
from utils.manuf import get_oui_vendor_name


class TestGetOuiVendorName(unittest.TestCase):
    def test_get_vendor_name(self):
        oui = '00:00:03'
        res = get_oui_vendor_name(oui, OUI_FILE)

        self.assertEqual(res, 'Xerox')

    def test_empty_file(self):
        oui = '00:00:00'
        res = get_oui_vendor_name(oui, '')

        self.assertEqual(res, False)

    def test_empty_oui(self):
        oui = ''
        res = get_oui_vendor_name(oui, OUI_FILE)

        self.assertEqual(res, False)

    def test_get_oui_unknown(self):
        oui = 'ZZ:ZZ:ZZ'
        res = get_oui_vendor_name(oui, OUI_FILE)

        self.assertEqual(res, False)
