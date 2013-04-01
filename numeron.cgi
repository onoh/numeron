#!/usr/bin/python
from wsgiref.handlers import CGIHandler
from numeron import app

CGIHandler().run(app)
