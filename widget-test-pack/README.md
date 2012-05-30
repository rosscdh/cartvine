### START UP ###

* We'll assume you are using a real machine (ubuntu/mac)
* windows your on your own there sorry.

1. cd into this dir
2. python -m SimpleHTTPServer 3000
3. browse to localhost:3000/index.html
4. profit

### NOTE ###

There are 3 degrees of javascript loading

1. loader.js - Really local file, found here in the same directory as this file
2. http://localhost:8000/static/widget/cartvine-loader.js - Running Django locally ./manage.py cartvine runserver_plus
3. http://shopify.app.cartvine.com/static/widget/cartvine-loader.js - The Live System
