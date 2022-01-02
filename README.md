# strukturen
This is the backend of "Strukturen". A service that will eventually offer you a machine readable representation of the federal public service of Germany. 

Including things like:
- Organisations
- Organisation Charts

This is the services that provides the main graphql backend, authentication and access management.

## Microservices
- [strukturen-ml](https://github.com/bundesAPI/strukturen-ml/) - Allows you to parse orgcharts with computer vision and nlp
- [strukturen-import-ui](https://github.com/bundesAPI/strukturen-import-ui/) User interface to manually review orgcharts before import
