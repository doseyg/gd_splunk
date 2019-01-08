#!/usr/bin/env python
######################
## Glen Dosey <doseyg@r-networks.net>
## Tested with MISP 2.4.98 and Splunk 7.1.3
## You must define which splunk fields to search for in MISP in the value splunk_fields

import sys
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators
import json, urllib2, ssl


@Configuration()
class mispSearchEventsCommand(StreamingCommand):
    """ %(synopsis)

    ##Syntax

    %(syntax)

    ##Description

    %(description)

    """
    def query_events_by_indicator_from_misp(self, indicator):
		## Input a value to search for in MISP, return all Event_ID, Galaxies matching the value. 
		##These variables should be passed in eventually
		MISP_HOST='172.16.135.143'
		MISP_KEY='XfuHyfCtKWTISsHsiDu10wWWDylpHQkHUWaowNi4'
		misp_id = "false"
		tags = "false"
		allowNonIDS = "false"
		matching_events = ""
		misp_info = ""
		## Start code
		#logger("Downloading indicators from MISP for type: %s" % indicator)
		MISP_URI = 'http://' + MISP_HOST + '/events/restSearch/'
		#MISP_POST = '{"request": {"eventid":["!51","!62"],"withAttachment":false,"tags":' + tags + ',"from":' + args.misp_start + ',"to":"' + args.misp_end + '"}}'
		MISP_POST = '{ "returnFormat": "json", "value":"' + indicator + '"}'
		#logger("Querying MISP at : %s" % MISP_URI)
		request = urllib2.Request(MISP_URI, MISP_POST)
		request.add_header("Authorization", MISP_KEY)
		request.add_header('Content-type', 'application/json')
		response = urllib2.urlopen(request, timeout=120, context=ssl._create_unverified_context())
		indicators = response.read()
		events = json.loads(indicators)
		#print("DEBUG: " + str(events))
		for event in events["response"]:
			#print(event["Event"]["id"])
			matching_events = matching_events + event["Event"]["id"] + " "
			misp_info = misp_info + event["Event"]["info"] + " "
		return(matching_events,misp_info)

	
	
	
	
    def stream(self, records):
		## Define a list of which fields from Splunk will be submitted to MISP for evaluation
		splunk_fields = ["srcIP","dstIP","md5","sha256","URL","filename","URI"]
		# For each event/record in splunk
		for record in records:
			#print("DEBUG " + record)
			record['misp_events'] = ""
			record['misp_info'] = ""
			fields = record.items()
			for field in fields:
				field_name = field[0]
				field_value=field[1]
				#print("DEBUG: field name is " + field_name)
				if field_name in splunk_fields:
					## ensure the field is not blank
					if len(field_value) > 3:
						#print("DEBUG: field value is " + field_value)
						results = self.query_events_by_indicator_from_misp(field_value)
						#print("DEBUG: " + str(results))
						## Concatenate the results together, as there may be several matching events in MISP
						record['misp_events'] = record['misp_events'] + " " + results[0]
						record['misp_info'] = record['misp_info'] + " " + results[1]
			yield record
		return


dispatch(mispSearchEventsCommand, sys.argv, sys.stdin, sys.stdout, __name__)
