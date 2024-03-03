# CampusFlow

CampusFlow is a student and administration management web-based system built for "Across" universities. It consists of an admin panel and a student dashboard.

## Technology Stack
- React JS - Frontend
- Django - Backend
- Blazegraph - Graph-based data storage for RDF
- Mysql - Database

## System Requirements
- Operating System
  - Windows
  - MacOS
  - Linux

- Software Requirements
  - [Mysql](https://dev.mysql.com/downloads/installer/)
  - [Blazegraph](https://github.com/blazegraph/blazegraph-python) 
  - [Python >= 3](https://www.python.org/downloads/)
  - [Nodejs >= 16](https://nodejs.org/en/download)

- Deployment Requirements
  - AWS RDF - For Mysql
  - AWS EC2 - For backend
  - AWS EC2 - For Blazegraph
  - AWS S3 - For frontend
  - Docker 

**Note:** Please use appropriate installation guides provided by the software providers based on your OS requirements

# Installation

### MySQL
We recommend using [mysqlworkbench](https://www.mysql.com/products/workbench/) to run the MySQL server locally

Once your MySQL server runs successfully, create an " across " database.
Make sure to update the settings.py with your MySQL configurations inside "DATABASES".

### Backend

Use the package manager pip or pip3 to run the backend. pip is usually part of python installation but in case you can't find pip command use this [link](https://pip.pypa.io/en/stable/)


Go to the folder Backend -> across and run the below commands
```bash
python3 -m pip install Django
```
```bash
python3 -m pip install -r requirements.txt
```
```bash
python3 manage.py runserver
```
**Note:** Please replace python3 with python incase python3 doesn't work on your system

_Hit the this URL on your browser to access the backend [LINK](http://127.0.0.1:8000/)_


### Frontend

Use the package manager npm to run the frontend. npm is part of NodeJS installation so you don't need to install it separately


Go to the folder Frontend -> across and run the below commands
```bash
npm install --force
```
```bash
npm run dev
```
_Hit this URL on your browser to access the webpage [LINK](http://localhost:5173/)_


### Blazegraph

Install the Blazegraph jar file from this [link](https://github.com/blazegraph/database/wiki/Quick_Start)

Go to the folder Blazegraph copy the installed jar and then run the following commands
```bash
java -server -Xmx4g -jar blazegraph.jar
```

_Hit this URL on your browser to access the blazegraph [LINK](http://localhost:9999/blazegraph/)_


## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)