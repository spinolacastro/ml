# This is a experimental Mercadolibre metrics client. It will fetch data from a given category and seller to further analysis.

* Load sql schema

`mysql < database.sql`

* Create a virtual env

`virtualenv .env && source .env/bin/activate`

* Install python libraries

`pip install -r requirements.txt`

* Fetch data

`./r.sh`