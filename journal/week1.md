# Week 1 — App Containerization

# Homework Tasks

## Setting Up Docker and Docker Compose with Cruddur

### Added Dockerfiles for Frontend and Backend

In following through the live stream for Week 1, I created the Dockerfiles within the following project folder location: 
`backend-flask/Dockerfile` and `frontend-react-js/Dockerfile`

```Backend Dockerfile
FROM python:3.10-slim-buster
WORKDIR /backend-flask
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_ENV=development
EXPOSE ${PORT}
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
```

```Frontend Dockerfile
FROM node:16.18
ENV PORT=3000
COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
EXPOSE ${PORT}
CMD ["npm", "start"]
```

### Built Images for Frontend and Backend

I ran the following command to build both images as per following through the guide in the livestream:

```sh Backend
docker build -t  backend-flask ./backend-flask
```

```sh Frontend
docker build -t frontend-react-js ./frontend-react-js
```

### Running Containers for Frotnend and Backend

I ran the following commands to get the containers running in continuing to following through the guide in the livestream:
*Note: Before running the frontend image, I ran `npm install` in the frontend directory to make sure all of the node packages were up-to-date.
*Note: I also made sure to set the identifiers for the frontend and backend urls in the backend container environment definition.

```sh Backend
docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask
```

```sh Frontend
docker run -p 3000:3000 -d frontend-react-js
```

### Created a docker-compose file

Created the `docker-compose.yml` file at the root of the project folder to orchestrate running both containers together at once:

```yaml
version: "3.8"
services:
  backend-flask:
    environment:
      FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
  frontend-react-js:
    environment:
      REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    volumes:
      - ./frontend-react-js:/frontend-react-js
# the name flag is a hack to change the default prepend folder
# name when outputting the image names
networks: 
  internal-network:
    driver: bridge
    name: cruddur
```

### Added DynamoDB Local and Postgres Containers

For a future date in the bootcamp, the docker compose file was prepared with Postgres and DynamoDB local containers for external reference.

``` Adding DynamoDB Local
  dynamodb-local:
    # https://stackoverflow.com/questions/67533058/persist-local-dynamodb-data-in-volumes-lack-permission-unable-to-open-databa
    # We needed to add user:root to get this working.
    user: root
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
    image: "amazon/dynamodb-local:latest"
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - "./docker/dynamodb:/home/dynamodblocal/data"
    working_dir: /home/dynamodblocal
```

```Adding Postgres
  db:
    image: postgres:13-alpine
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - '5432:5432'
    volumes: 
      - db:/var/lib/postgresql/data

volumes:
  db:
    driver: local
```

In addition, I made sure to install the Postgres Client by including it as a task in the Gitpod.yml file:

```sh
  - name: postgres
    init: |
      curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
      echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
      sudo apt update
      sudo apt install -y postgresql-client-13 libpq-dev
```

# Homework Challenges

## Run the dockerfile CMD as an external script

## Push and tag a image to DockerHub

## Use multi-stage building for a Dockerfile build

## Learn how to install Docker on your localmachine and get the same containers running outside of Gitpod / Codespaces

## Launch an EC2 instance that has docker installed, and pull a container to demonstrate you can run your own docker processes
