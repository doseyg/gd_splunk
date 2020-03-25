This splunk app uses the web api of the caching-whois-proxy available at http://github.com/doseyg/caching-whois-proxy.
Please ensure they caching-whois-proxy is working before trying to implement this app. 

##Installation
These instructions work for a single node Splunk instance. If clustered and using a deplyment server, refer to Splunk docs or your Splunk admin.
Copy the contents of this whois folder into the $SPLUNK_HOME/etc/apps/ folder. 
Copy the splunklib folder from the SPlunk Python SDK into the $SPLUNK_HOME/etc/apps/whois/bin folder
Restart Splunk.

##Usage
An example splunk query would be:
index=weblogs | whois lookupfield=source_ip 
The data in the soure_ip field will be submitted to whois and the resulting values will be placed in fields name source_ip_whois_<something>
Typical added fields are:
-whois_domain_name
-whois_name
-whois_org
-whois_registrar
-whois_updated_date
-whois_creation_date
-whois_emails
-whois_address
-whois_city
-whois_country

##Use your own API
Alternatively, you can easily use this Splunk app with the web api of your own whois lookup tools. Change the syntax of the query in bin/whois.py
