#!/usr/bin/env python3

# Copyright (C) 2017-2019 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

import unittest
from btclib import der


class TestDER(unittest.TestCase):
    def test_der(self):

        sighash_all = b'\x01'

        sig73 = 2**256 - 1, 2**256 - 1
        sig72 = 2**255 - 1, 2**256 - 1
        sig71 = 2**255 - 1, 2**255 - 1
        sig71b = 2**255 - 1, 2**248 - 1
        sig70 = 2**255 - 1, 2**247 - 1
        sig69 = 2**247 - 1, 2**247 - 1
        sigs = [sig73, sig72, sig71, sig71b, sig70, sig69]

        for sig in sigs:
            DER = der.encode(sig, sighash_all)
            sig2, sighash_all2 = der.decode(DER)
            self.assertEqual(sig, sig2)
            self.assertEqual(sighash_all, sighash_all2)
        # with the last one

        # DER signature size should be in [9, 73]
        DER2 = DER + b'\x00' * 10
        self.assertRaises(ValueError, der.decode, DER2)

        # DER signature must be of type 0x30 (compound)
        DER2 = b'\x00' + DER[1:]
        self.assertRaises(ValueError, der.decode, DER2)

        # Declared signature size does not match with size
        DER2 = DER[:1] + b'\x00' + DER[2:]
        self.assertRaises(ValueError, der.decode, DER2)

        Rsize = DER[3]
        # Zero-size integers are not allowed for r
        DER2 = DER[:3] + b'\x00' + DER[4:]
        self.assertRaises(ValueError, der.decode, DER2)

        # Length of the s element must be inside the signature
        DER2 = DER[:3] + b'\x80' + DER[4:]
        self.assertRaises(ValueError, der.decode, DER2)

        # Zero-size integers are not allowed for s
        DER2 = DER[:Rsize+5] + b'\x00' + DER[Rsize+6:]
        self.assertRaises(ValueError, der.decode, DER2)

        # Signature size does not match with elements
        DER2 = DER[:Rsize+5] + b'\x4f' + DER[Rsize+6:]
        self.assertRaises(ValueError, der.decode, DER2)

        # r element must be an integer
        DER2 = DER[:2] + b'\x00' + DER[3:]
        self.assertRaises(ValueError, der.decode, DER2)

        # Negative numbers are not allowed for r
        DER2 = DER[:4] + b'\x80' + DER[5:]
        self.assertRaises(ValueError, der.decode, DER2)

        # Invalid null bytes at the start of r
        DER2 = DER[:4] + b'\x00\x00' + DER[6:]
        self.assertRaises(ValueError, der.decode, DER2)

        # s element must be an integer
        DER2 = DER[:Rsize+4] + b'\x00' + DER[Rsize+5:]
        self.assertRaises(ValueError, der.decode, DER2)

        # Negative numbers are not allowed for s
        DER2 = DER[:Rsize+6] + b'\x80' + DER[Rsize+7:]
        self.assertRaises(ValueError, der.decode, DER2)

        # Invalid null bytes at the start of s
        DER2 = DER[:Rsize+6] + b'\x00\x00' + DER[Rsize+8:]
        self.assertRaises(ValueError, der.decode, DER2)

        # sighash size > 1
        self.assertRaises(ValueError, der.encode, sig, sighash_all + b'\x01')

        # negative signature element
        sig2 = -1 , sig[1]
        self.assertRaises(ValueError, der.encode, sig2, sighash_all)


if __name__ == "__main__":
    # execute only if run as a script
    unittest.main()
