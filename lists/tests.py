# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

class SmokeTest(TestCase):

	def test_bad_maths(self):
		self.assertEqual(1+1, 3)