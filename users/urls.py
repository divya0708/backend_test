# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.contrib import admin
from users import views

urlpatterns = [
	url(r'^add_user_details$', views.adding_user_details, name="adding_user_details"),
	url(r'^get_user_details$', views.getting_user_details, name="getting_user_details"),
	]