## This is the convertor app to covert PDF to CSV/XLSX file

### Steps to start the app:

##### Firstly you need to clone git repository:
`git clone https://github.com/vitossss/converter-files.git`

##### Then you need to create .env file in project folder

##### **Warning: your .env file must looks like .env.example**
For example: `DJANGO_SECRET_KEY='here_you_put_random_secret_key'`

##### The last step is start docker compose up command
`docker compose up`

After starting the app go to `/api/csv` endpoint and put `COMMANDE STOCK BRUXELLES.pdf` and send it.

As response, you will get a csv with table data from pdf
