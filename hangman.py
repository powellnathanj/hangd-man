#!/usr/bin/env python

from twisted.application import service
import hangd

application = service.Application("Hangd")
hangService = hangd.HangService()
hangService.setServiceParent(application)

