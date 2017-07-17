# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class List(models.Model):
	pass

class Item(models.Model):
	text = models.TextField(default='')
	list = models.ForeignKey(List, default = None)


