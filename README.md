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
  - [Blazegraph](https://blazegraph.com/) 
  - [Python >= 3](https://www.python.org/downloads/)
  - [Nodejs >= 16](https://nodejs.org/en/download)

- Deployment Requirements
  - AWS RDF - For Mysql
  - AWS EC2 - For backend
  - AWS EC2 - For Blazegraph
  - AWS S3 - For frontend
  - Docker 

**Note:** Please use appropriate installation guides provided by the software providers based on your OS requirements

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

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