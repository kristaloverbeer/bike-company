# Gateway service

This API service allows you to retrieve all bikes currently existing and retrieve one bike by its id.

## Usage

To launch the stack:
```bash
make run
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
GET http://localhost:8080/

GET http://localhost:8080/hello
```

Ping route:
```python
GET http://localhost:8080/ping
```

To retrieve all bikes:
```python
GET http://localhost:8080/v1/bikes
```

To retrieve a bike:
```python
GET http://localhost:8080/v1/bikes/bb3398hl52n3nnikkt90
```


##TODO List

- Unit tests
- Integration tests
- Performance tests
- Better logging across the code base
- Monitoring
