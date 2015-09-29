#!flask/bin/python
from flask import Flask, jsonify
import ConfigParser
import io


app = Flask(__name__)

cfile="config/services.ini"

# Load the configuration file
with open(cfile) as f:
	sample_config = f.read()
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.readfp(io.BytesIO(sample_config))


app = Flask(__name__)

@app.route('/')
def index():
	services=""
	html="<html><head><title>Services</title></head><body>"
	for section in config.sections():
		html=html + "<fieldset><legend>Command = [<a href='/%s'>%s</a>]</legend><form action='/%s'><dl>\n" % (section,section,section)
		for option in config.options(section):
			if option == 'command':
				html=html + "<dt>command line</dt><dd><code>&gt; %s</code></dd>\n" % (config.get(section, option))
			else:
				key=option
				val=config.get(section, option)
				html=html + "<dt>?<i>%s</i>=</dt><dd><input size=5 name='%s' value='%s' /></dd>\n" % (key, key, val)
		html=html + "<dd><input type=submit value='Call [%s]'></dd></dl></form></fieldset>\n" % (section)
	html=html + "</dl></body></html>"
	return html

@app.route('/<command>',methods=['GET'])
def get_command(command):
	for section in config.sections():
		if section == command:
			# first take default settings
			for options in config.options(command):
				print("- %s = %s" % (options,config.get(section, options)))
			# then take URL params
			# check for command line and execute
			# check for command URL and execute
	return "Executing [%s]" % command


if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
	