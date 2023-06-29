import unittest, os, sys
sys.path.append('.')

from ASN1Der import DerIBase

data_127 = "3059301306072A8648CE3D020106082A811CCF5501822D034200046A826E79032BA6144FA1EB22F4F2BA3D2B77EBDC54789C1EF15B64FBCFE7A259E771DDD2FE6DDB377B1A9820B394F58AFA2BF02226EC5DAEFACC14B2A22D4E11"

assert_127_result = {
    "tag": "30",
    "length": "59",
    "value": "301306072A8648CE3D020106082A811CCF5501822D034200046A826E79032BA6144FA1EB22F4F2BA3D2B77EBDC54789C1EF15B64FBCFE7A259E771DDD2FE6DDB377B1A9820B394F58AFA2BF02226EC5DAEFACC14B2A22D4E11"
}

data_129 = "0381810047eb995adf9e700dfba73132c15f5c24c2e0bfc624af15660eb86a2eab2bc4971fe3cbdc63a525ecc7b428616636a1311bbfddd0fcbf1794901de55ec7115ec9559feba33e14c799a6cbbaa1460f39d444c4c84b760e205d6da9349ed4d58742eb2426511490b40f065e5288327a9520a0fdf7e57d60dd72689bf57b058f6d1e"

assert_129_result = {
    "tag": "03",
    "length": "8181",
    "value": "0047eb995adf9e700dfba73132c15f5c24c2e0bfc624af15660eb86a2eab2bc4971fe3cbdc63a525ecc7b428616636a1311bbfddd0fcbf1794901de55ec7115ec9559feba33e14c799a6cbbaa1460f39d444c4c84b760e205d6da9349ed4d58742eb2426511490b40f065e5288327a9520a0fdf7e57d60dd72689bf57b058f6d1e"
}

class TestDerIBase(unittest.TestCase):

    def test_127_data(self):
        test = DerIBase(data_127)
        self.assertEqual(test.tag, assert_127_result["tag"])
        self.assertEqual(test.length, assert_127_result["length"])
        self.assertEqual(test.value, assert_127_result["value"])

    def test_129_data(self):
        test = DerIBase(data_129)
        self.assertEqual(test.tag, assert_129_result["tag"])
        self.assertEqual(test.length, assert_129_result["length"])
        self.assertEqual(test.value, assert_129_result["value"])

if __name__ == "__main__":
    unittest.main()