# -*- coding: utf-8 -*-
# Copyright (c) nexB Inc. and others.
# This code is based on Tomaž Šolc's fork of David Wilson's code originally at
# https://www.tablix.org/~avian/git/publicsuffix.git
#
# Copyright (c) 2014 Tomaž Šolc <tomaz.solc@tablix.org>
#
# David Wilson's code was originally at:
# from http://code.google.com/p/python-public-suffix-list/
#
# Copyright (c) 2009 David Wilson
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
# The Public Suffix List vendored in this distribution has been downloaded
# from http://publicsuffix.org/public_suffix_list.dat
# This data file is licensed under the MPL-2.0 license.
# http://mozilla.org/MPL/2.0/


from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from ..fast_psl.core import PublicSuffixList


class TestPublicSuffix(unittest.TestCase):

    def test_get_sld_from_empty_list(self):
        psl = PublicSuffixList()
        assert 'com' == psl.get_public_suffix('com')
        assert 'com' == psl.get_public_suffix('COM')
        assert 'com' == psl.get_public_suffix('.com')
        assert 'com' == psl.get_public_suffix('a.example.com')
        # expect private suffix to still match
        assert '12chars.dev' == psl.get_public_suffix('a.12chars.dev')

    def test_get_sld_from_empty_list_in_strict_mode(self):
        psl = PublicSuffixList(strict=True)
        assert None == psl.get_public_suffix('com')
        # expect private suffix to raise a ValueError
        with self.assertRaises(ValueError):
            psl.get_public_suffix('12chars.dev')
        


    def test_get_sld_from_list(self):
        psl = PublicSuffixList()
        assert 'com' == psl.get_public_suffix('a.example.com')
        assert 'com' == psl.get_public_suffix('a.a.example.com')
        assert 'com' == psl.get_public_suffix('a.a.a.example.com')
        assert 'com' == psl.get_public_suffix('A.example.com')
        assert 'com' == psl.get_public_suffix('.a.a.example.com')

    def test_get_sld_from_list_with_fqdn(self):
        psl = PublicSuffixList()
        assert 'com' == psl.get_sld('example.com.')

    def test_get_sld_from_list_with_unicode(self):
        psl = PublicSuffixList()
        assert u'\u0440\u0444' == psl.get_sld(u'\u0440\u0444')
        assert u'\u0440\u0444' == psl.get_public_suffix(u'example.\u0440\u0444')
        assert u'\u0440\u0444' == psl.get_public_suffix(u'a.example.\u0440\u0444')
        assert u'\u0440\u0444' == psl.get_public_suffix(u'a.a.example.\u0440\u0444')

class TestPublicSuffixUsingTheCurrentVendoredPSL(unittest.TestCase):

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_mixed_case(self):
        psl = PublicSuffixList()
        assert 'com' == psl.get_public_suffix('COM')
        assert 'com' == psl.get_public_suffix('example.COM')
        assert 'com' == psl.get_public_suffix('WwW.example.COM')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_leading_dot(self):
        psl = PublicSuffixList()
        assert 'com' == psl.get_public_suffix('.com')
        with self.assertRaises(ValueError):
            psl.get_public_suffix('.example')
        assert 'com' == psl.get_public_suffix('.example.com')
        with self.assertRaises(ValueError):
            psl.get_public_suffix('.example.example')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_unlisted_tld(self):
        psl = PublicSuffixList()
        with self.assertRaises(ValueError):
            psl.get_public_suffix('example')
        with self.assertRaises(ValueError):
            psl.get_public_suffix('example.example')
        with self.assertRaises(ValueError):
            psl.get_public_suffix('b.example.example')
        with self.assertRaises(ValueError):
            psl.get_public_suffix('a.b.example.example')


    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_one_rule(self):
        psl = PublicSuffixList()
        assert 'biz' == psl.get_public_suffix('biz')
        assert 'biz' == psl.get_public_suffix('domain.biz')
        assert 'biz' == psl.get_public_suffix('b.domain.biz')
        assert 'biz' == psl.get_public_suffix('a.b.domain.biz')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_two_level_rules(self):
        psl = PublicSuffixList()
        assert 'com' == psl.get_public_suffix('com')
        assert 'com' == psl.get_public_suffix('example.com')
        assert 'com' == psl.get_public_suffix('b.example.com')
        assert 'com' == psl.get_public_suffix('a.b.example.com')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_two_level_uk_rules(self):
        psl = PublicSuffixList()
        assert 'uk.com' == psl.get_public_suffix('uk.com')
        assert 'uk.com' == psl.get_public_suffix('example.uk.com')
        assert 'uk.com' == psl.get_public_suffix('b.example.uk.com')
        assert 'uk.com' == psl.get_public_suffix('a.b.example.uk.com')
        assert 'ac' == psl.get_public_suffix('test.ac')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_wildcard_rule(self):
        psl = PublicSuffixList()
        assert 'er' == psl.get_public_suffix('er')
        assert 'c.er' == psl.get_public_suffix('c.er')
        assert 'b.c.er' == psl.get_public_suffix('b.c.er')
        assert 'b.c.er' == psl.get_public_suffix('a.b.c.er')

    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_japanese_domain(self):
        psl = PublicSuffixList()
        assert 'jp' == psl.get_public_suffix('jp')
        assert 'jp' == psl.get_public_suffix('test.jp')
        assert 'jp' == psl.get_public_suffix('www.test.jp')
        assert 'jp' == psl.get_public_suffix('ac.jp')
        assert 'jp' == psl.get_public_suffix('test.ac.jp')
        assert 'jp' == psl.get_public_suffix('www.test.ac.jp')
        assert 'jp' == psl.get_public_suffix('kobe.jp')
        assert 'jp' == psl.get_public_suffix('c.kobe.jp')
        assert 'jp' == psl.get_public_suffix('b.c.kobe.jp')
        assert 'jp' == psl.get_public_suffix('a.b.c.kobe.jp')



    def test_get_sld_from_builtin_full_publicsuffix_org_list_with_us_k12(self):
        psl = PublicSuffixList()
        assert 'ak.us' == psl.get_sld('ak.us')
        assert 'ak.us' == psl.get_sld('test.ak.us')
        assert 'ak.us' == psl.get_sld('www.test.ak.us')
        assert 'k12.ak.us' == psl.get_sld('k12.ak.us')
        assert 'k12.ak.us' == psl.get_sld('test.k12.ak.us')
        assert 'k12.ak.us' == psl.get_sld('www.test.k12.ak.us')


class TestPublicSuffixGetSldIdna(unittest.TestCase):

    def test_get_sld_idna_encoded(self):
        # actually the default
        psl = PublicSuffixList()
        assert 'com.cn' == psl.get_sld('xn--85x722f.com.cn')
        assert 'xn--55qx5d.cn' == psl.get_sld('xn--85x722f.xn--55qx5d.cn')
        assert 'xn--55qx5d.cn' == psl.get_sld('www.xn--85x722f.xn--55qx5d.cn')
        assert 'xn--55qx5d.cn' == psl.get_sld('shishi.xn--55qx5d.cn')

    def test_get_sld_with_utf8_encoded(self):
        # uses the list provided utf-8 defaults
        psl = PublicSuffixList()
        assert u'com.cn' == psl.get_sld(u'食狮.com.cn')
        assert u'公司.cn' == psl.get_sld(u'食狮.公司.cn')
        assert u'公司.cn' == psl.get_sld(u'www.食狮.公司.cn')
        assert u'公司.cn' == psl.get_sld(u'shishi.公司.cn')

    def test_get_sld_exceptions(self):
        psl = PublicSuffixList()
        # www is the exception
        assert 'www.ck' == psl.get_sld('www.www.ck')
        assert 'this.that.ck' == psl.get_sld('this.that.ck')

#     def test_get_sld_no_wildcard(self):
#         psl = PublicSuffixList()
#         # test completion when no wildcards should be processed
#         assert 'com.pg' == psl.get_sld('telinet.com.pg', wildcard=False)
#         expected = 'ap-southeast-1.elb.amazonaws.com'
#         result = psl.get_sld('blah.ap-southeast-1.elb.amazonaws.com', wildcard=False)
#         assert expected == result

#     def test_get_sld_top_convenience_function_is_the_same_as_PublicSuffixList_method(self):
#         psl = PublicSuffixList()
#         # these functions should be identical
#         assert psl.get_sld('www.google.com') == publicsuffix.get_sld('www.google.com')
#         assert psl.get_sld('www.test.ak.us') == publicsuffix.get_sld('www.test.ak.us')

#     def test_get_tld_returns_correct_tld_or_etld(self):
#         psl = PublicSuffixList()
#         assert 'com' == psl.get_tld('com')
#         assert 'kobe.jp' == psl.get_tld('city.kobe.jp')
#         assert 'kobe.jp' == psl.get_tld('kobe.jp')
#         assert 'amazonaws.com' == psl.get_tld('amazonaws.com')
#         assert 'com.pg' == psl.get_tld('telinet.com.pg', wildcard=True)
#         assert 'pg' == psl.get_tld('telinet.com.pg', wildcard=False)
#         assert 'com.pg' == psl.get_tld('com.pg', wildcard=True)
#         assert 'pg' == psl.get_tld('com.pg', wildcard=False)
#         assert 'co.uk' == psl.get_tld('telinet.co.uk', wildcard=False)
#         assert 'co.uk' == psl.get_tld('co.uk', wildcard=True)
#         assert 'co.uk' == psl.get_tld('co.uk', wildcard=False)
#         assert None == psl.get_tld('blah.local', strict=True)
#         assert None == psl.get_tld('blah.local', wildcard=False)
#         assert 'local' == psl.get_tld('blah.local')

#     def test_get_tld_returns_correct_tld_or_etld_for_fqdn(self):
#         psl = PublicSuffixList()
#         assert 'com' == psl.get_tld('www.foo.com.')

#     def test_get_tld_returns_correct_tld_or_etld_for_root_domain(self):
#         psl = PublicSuffixList()
#         assert '' == psl.get_tld('.')

#     def test_get_tld_returns_correct_tld_or_etld_for_empty_string(self):
#         psl = PublicSuffixList()
#         assert None == psl.get_tld('')

#     def test_PublicSuffixList_tlds_is_loaded_correctly(self):
#         psl = PublicSuffixList()
#         assert psl.tlds


# class TestPublicSuffixGetSld(unittest.TestCase):

#     def test_get_sld_backward_compatibility(self):
#         psl = PublicSuffixList()
#         assert 'com' == psl.get_sld('com')
#         assert 'foo.com' == psl.get_sld('foo.com')
#         assert 'foo.co.jp' == psl.get_sld('foo.co.jp')
#         assert 'co.jp' == psl.get_sld('co.jp')
#         assert 'jp' == psl.get_sld('jp')

#     def test_get_sld_backward_compatibility_strict_and_wildcard_flags(self):
#         psl = PublicSuffixList()
#         assert 'local' == psl.get_sld('local')
#         assert 'local' == psl.get_sld('foo.local')
#         assert None == psl.get_sld('local', strict=True)
#         assert None == psl.get_sld('foo.local', strict=True)
#         assert 'local' == psl.get_sld('local', wildcard=False)
#         assert 'local' == psl.get_sld('foo.local', strict=False)

#     def test_get_sld_backward_compatibility_sld_for_empty_string(self):
#         psl = PublicSuffixList()
#         assert None == psl.get_sld('')
#         assert None == psl.get_sld('', strict=True)
#         assert None == psl.get_sld('', wildcard=False)

#     def test_get_sld_backward_compatibility_sld_for_fqdn(self):
#         psl = PublicSuffixList()
#         assert 'foo.com' == psl.get_sld('www.foo.com.')

#     def test_get_sld_backward_compatibility_sld_for_root_domain(self):
#         psl = PublicSuffixList()
#         assert '' == psl.get_sld('.')
#         assert None == psl.get_sld('.', strict=True)
#         assert '' == psl.get_sld('.', wildcard=False)


if __name__ == '__main__':
    unittest.main('tests')