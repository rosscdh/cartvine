# -*- coding: UTF-8 -*-
from django.contrib import admin
from models import Widget, WidgetInfo, WidgetShop


admin.site.register([Widget, WidgetInfo, WidgetShop])
