# Vehicle-Allocation-System

## API Collection

This project is an API collection that manages vehicle and employee allocations using FastAPI and MongoDB. It allows for the creation, retrieval, updating, and deletion of allocations.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started with Docker](#getting-started-with-docker)
- [API Endpoints](#api-endpoints)
- [Allocation Functionality](#allocation-functionality)
- [Running the Tests](#running-the-tests)
- [License](#license)

## Prerequisites

- Docker
- Docker Compose
- Python 3.12 (for local development)

## Getting Started with Docker

1. **Clone the Repository**

   ```bash
   git clone https://github.com/WazedKhan/Vehicle-Allocation-System
   cd Vehicle-Allocation-System

## Build the Docker Images and Run the Services

Use the following command to build the Docker images:
- ```docker-compose build```
- ```docker-compose up```

Running the Tests
To run the tests, you can use the following command:

```sh
docker-compose exec app python -m unittest discover -s tests
```