# Requirements

This application require docker and docker-compose to be installed on your machine.

## Exporting main variables

This variables are used to configure the application.


```bash
export JWT_SECRET_KEY="my-32-character-ultra-secure-and-ultra-long-secret"
export ENV="dev"
export MONGO_URI="mongodb://localhost"
export PYTHONPATH=./app
```

## Usage

```bash
docker-compose up -d --build
```

## Testing
Run the following command in root directory.

```bash
pytest
```