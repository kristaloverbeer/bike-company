# Bike service

This API service allows you to retrieve all bikes currently existing and retrieve one bike by its id.

## Usage

To launch the stack:
```bash
make run
```

To upgrade the database to the latest schema:
```bash
make upgrade
```

To execute the different tests suites:
```bash
make typing-check
make syntax-check
make tests
```

To enter the API container:
```bash
make sh
```

To stop the stack:
```bash
make stop
```

To clean the containers created:
```bash
make clean
```

To clean old built images that are not used anymore:
```bash
make clean-dangling-images
```

# Endpoints

Index route:
```python
GET http://localhost:8081/

GET http://localhost:8081/hello
```

Ping route:
```python
GET http://localhost:8081/ping
```

For tests purposes, this endpoint allows to post bike data (through Postman for instance):
```python
POST http://localhost:8081/v1/bikes

[
  {
    "id": "bb3398hl52n3nnikkt90",
    "location": {
      "type": "Point",
      "coordinates": [
        2.299104,
        48.854996
      ]
    }
  },
  {
    "id": "bb3398hl52n3nnikkt9g",
    "location": {
      "type": "Point",
      "coordinates": [
        2.34467,
        48.88958
      ]
    }
  }
]
```

To retrieve all bikes:
```python
GET http://localhost:8081/v1/bikes
```

To retrieve a bike:
```python
GET http://localhost:8081/v1/bikes/bb3398hl52n3nnikkt90
```

##TODO List

- Unit tests
- Integration tests
- Performance tests
- Better logging across the code base
- Monitoring
