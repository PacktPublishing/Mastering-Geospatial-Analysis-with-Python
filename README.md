## [Get this title for $10 on Packt's Spring Sale](https://www.packt.com/B07333?utm_source=github&utm_medium=packt-github-repo&utm_campaign=spring_10_dollar_2022)
-----
For a limited period, all eBooks and Videos are only $10. All the practical content you need \- by developers, for developers

# Mastering Geospatial Analysis with Python
This is the code repository for [Mastering Geospatial Analysis with Python](https://www.packtpub.com/application-development/mastering-geospatial-analysis-python?utm_source=github&utm_medium=repository&utm_campaign=9781788293334), published by [Packt](https://www.packtpub.com/?utm_source=github). It contains all the supporting project files necessary to work through the book from start to finish.
## About the Book
Python comes with a host of open source libraries and tools that help you work on professional geoprocessing tasks without investing in expensive tools. This book will introduce Python developers, both new and experienced, to a variety of new code libraries that have been developed to perform geospatial analysis, statistical analysis, and data management. This book will use examples and code snippets that will help explain how Python 3 differs from Python 2, and how these new code libraries can be used to solve age-old problems in geospatial analysis.

You will begin by understanding what geoprocessing is and explore the tools and libraries that Python 3 offers. You will then learn to use Python code libraries to read and write geospatial data. You will then learn to perform geospatial queries within databases and learn PyQGIS to automate analysis within the QGIS mapping suite. Moving forward, you will explore the newly released ArcGIS API for Python and ArcGIS Online to perform geospatial analysis and create ArcGIS Online web maps. Further, you will deep dive into Python Geospatial web frameworks and learn to create a geospatial REST API.

## Instructions and Navigation
All of the code is organized into folders. Each folder starts with a number followed by the application name. For example, Chapter02.



The code will look like the following:
```
import requests

url='http://coagisweb.cabq.gov/arcgis/rest/services/public/PublicArt/MapServer/0/query'

params={"where":"1=1","outFields":"*","outSR":"4326","f":"json"}

r=requests.get(url,params=params)

data=r.json()

data["features"][0]
```

This book is for anyone who works with location information and Python. Students, developers, and geospatial professionals can all use this reference book, as it covers GIS data management, analysis techniques, and code libraries built with Python 3.

## Related Products
* [Mapping with ArcGIS Pro](https://www.packtpub.com/application-development/mapping-arcgis-pro?utm_source=github&utm_medium=repository&utm_campaign=9781788298001)

* [ArcGIS Pro 2.x Cookbook](https://www.packtpub.com/application-development/arcgis-pro-2x-cookbook?utm_source=github&utm_medium=repository&utm_campaign=9781788299039)

* [Building Web and Mobile ArcGIS Server Applications with JavaScript - Second Edition](https://www.packtpub.com/application-development/building-web-and-mobile-arcgis-server-applications-javascript-second-edition?utm_source=github&utm_medium=repository&utm_campaign=9781787280526)
