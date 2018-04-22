# Trip service

This API service allows you to start and/or stop a trip and update the history locations of each bike.

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
GET http://localhost:8082/

GET http://localhost:8082/hello
```

Ping route:
```python
GET http://localhost:8082/ping
```

To start a trip:
```python
PUT http://localhost:8082/v1/trips/start/bb3398hl52n3nnikkt90
```

To stop a trip:
```python
PATCH http://localhost:8082/v1/trips/end/bb3398hl52n3nnikkt90
```

##TODO List

- Unit tests
- Integration tests
- Performance tests
- Better logging across the code base
- Monitoring
- Normalize database model
