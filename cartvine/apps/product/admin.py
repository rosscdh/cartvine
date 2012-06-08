# -*- coding: UTF-8 -*-
from django.contrib import admin
from models import Product, ProductVariant


admin.site.register([Product, ProductVariant])

