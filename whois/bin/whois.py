#!/usr/bin/env python
# coding=utf-8
#

from __future__ import absolute_import, division, print_function, unicode_literals
#import app
import os,sys

splunkhome = os.environ['SPLUNK_HOME']
sys.path.append(os.path.join(splunkhome, 'etc', 'apps', 'searchcommands_app', 'lib'))
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators
from splunklib import six
import requests, json

caching_whois_proxy = "http://127.0.0.1:8003/api?query="

@Configuration()
class whoisCommand(StreamingCommand):
    lookupfield = Option(
        doc='''
        **Syntax:** **lookupfield=***<fieldname>*
        **Description:** Name of the field to perform whois lookup on''',
        require=True, validate=validators.Fieldname())

    def stream(self, records):
        self.logger.debug('WhoisLookup: %s', self)  # logs command line
        for record in records:
            whois_result={}
            new_whois_result={}
            request = caching_whois_proxy + record[self.lookupfield]
            resp = requests.get(request)
            whois_result = json.loads(resp.text)
            if whois_result is not None:
                for k, v in whois_result.iteritems():
                ## Iterate through every field returned by the whois lookup, prepend them whois_ before adding to splunk result
                       nk = "whois_" + k
                       new_whois_result[nk]=v
                record.update(new_whois_result)
            yield record

dispatch(whoisCommand, sys.argv, sys.stdin, sys.stdout, __name__)
