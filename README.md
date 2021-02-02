# Twitch Widgets
A simple web server that builds overlays that you can insert into your stream using OBS browser plugin.

# Installation
You will need package `requests`. Can be installed using `pip install requests`. Only tested with python 3.8.

Copy the config file and replace the placeholder token with your actual goal token from streamlabs.
```
cp template_variables.json.sample template_variables.json
```

# Run
To run the server simply launch `python3 serve.py` and point your browser at `http://localhost:8080/followers`.


