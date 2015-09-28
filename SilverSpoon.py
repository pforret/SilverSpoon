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
    return "Hello, World!"

@app.route('/<command>',methods=['GET'])
def get_command(command):
	# List all contents
	print("Reading from [%s]" % command)
	for section in config.sections():
		if section == command:
			# command was found - now execute it
			for options in config.options(command):
				print("- %s = %s" % (options,config.get(section, options)))
	return "Executing [%s]" % command


if __name__ == '__main__':
	app.run(debug=True)