# -*- coding: UTF-8 -*-
from django.contrib import admin
from models import Webhook, OrderCreatePostback


admin.site.register([Webhook, OrderCreatePostback])

