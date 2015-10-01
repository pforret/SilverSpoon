#!flask/bin/python
from flask import Flask, jsonify, request
import ConfigParser, io, re, requests, os,subprocess


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
			p = re.compile( '(\[\d+\])')
			short=p.sub('',option)
			if short == 'command':
				key=option
				val=config.get(section, option)
				html=html + "<dt>command line</dt><dd><code>&gt; %s</code></dd>\n" % val
			else:
				key=option
				val=config.get(section, option)
				html=html + "<dt>?<i>%s</i>=</dt><dd><input size=5 name='%s' value='%s' /></dd>\n" % (key, key, val)
		html=html + "<dd><input type=submit value='Call [%s]'></dd></dl></form></fieldset>\n" % (section)
	html=html + "</dl></body></html>"
	return html

@app.route('/<command>',methods=['GET'])
def get_command(command):
	commands=[] # array
	for section in config.sections():
		if section == command:
			# first take default settings
			params={} # dictionary
			for key in config.options(command):
				p = re.compile( '(\[\d+\])')
				short=p.sub('',key)
				if short == 'command':
					val=config.get(section, key)
					commands.append(val)
				else:
					val=config.get(section, key)
					params[key]=val
			# then take URL params
			for key in request.args:
				val=request.args.get(key)
				params[key]=val
			for key in request.form:
				val=request.form.get(key)
				params[key]=val
			## now execute
			for command in commands:
				#print "before:",command
				for key in params:
					val=params[key]
					command=command.replace("{%s}"%key,val)
				if command.startswith('http://') or command.startswith("https://"):
					print "Call URL: [%s]" % command
					r = requests.get(command)
				else:
					print "subprocess: [%s]" % command
					os.system(command)

	return "Executing [%s]" % command


if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
	