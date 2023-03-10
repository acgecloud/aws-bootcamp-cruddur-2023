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

Separate from explicitly including the CMD command that runs upon the launch of a container, the CMD command can also be specified from the command line as an argument passed to the `docker run` command. As a result, I tested running both the frontend and backend cnotaines by creating two external bash scripts, which would run the Dockerfile CMD for each container. I have attached these two scripts at the locations `/backend-flask/external-script-cmd-backend.sh` and `/frontend-react-js/external-script-cmd-frontend.sh` in the project folder:
*Note: The argument `$1` in the bash script refers to an argument for the specific container tags included when running `bash external-script.sh [tag-name-for-$1]`

``` Frontend Script
#!/bin/bash
# runs the starting frontend task
# Enter the appropriate tag name for running this script
docker run -p 3000:3000 -d frontend-react-js:$1 npm start
```

```Backend Script
#!/bin/bash
# runs the starting backend task
# Enter the appropriate tag name for running this script
docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask:$1 python3 -m flask run --host=0.0.0.0 --port=4567
```

## Push and tag a image to DockerHub

To push and tag an image to Dockerhub, I created a Dockerhub account and downloaded the Docker Desktop application to get started. I pulled the docker/getting-started base image to practice with getting acquainted with the tagging and pushing features to Dockerhub. After pulling the image `docker run -d -p 80:80 docker/getting-started`, I then re-tagged the image `docker tag docker/getting-started acgecloud/docker-tutorial-acge:getting-started-v1` and then pushed it `docker tag docker/getting-started acgecloud/docker-tutorial-acge:getting-started-v1` to a private repository within the Dockerhub account I recently created to practice with pushing and tagging docker images. I have attached an image of the result as follows:
*Note: Docker Docs were very useful in practicing features, and used for reference: [Docker Repo Documentation](https://docs.docker.com/docker-hub/repos/)

![Docker Image Tagged and Pushed](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week1/docker-image-tagging-and-pushing-to-tag.PNG)

## Use multi-stage building for a Dockerfile build

Multi-stage building refers to the use of using multiple base images in succession, transferring generated artifacts across layers from each image until they are finally copied to the final image used for the production build / compilation. I have learned that this is a resourceful way to only keep the relevant files, binaries, packages, etc. in the final build, which reduces the size of the final image and improves its overall portability. I have referred to various resources for learning how to use multi-stage building, which I am including here as reference: [Understanding Multi-Stage Building](https://www.youtube.com/watch?v=zpkqNPwEzac) and [Learning from a Practical Example of Multi-Stage Building with NodeJS](https://www.youtube.com/watch?v=26ABfSQ7UeU). I was able to learn from these tutorials to modify the Dockerfiles for both frontend and backend. I have included these updates in the Dockerfile within each respective folder (/backend-flask/Dockerfile) and (/frontend-react-js/Dockerfile) in the project folder.

### Backend Multi-Stage
I decided to use a virtual environment for the python backend to keep all of the packages in one place to make it easier for copying over to the final compiler image. 
After installing the packages and setting up the requirements, I used an Alpine base image for the final compilation, which is a lighterweight image to reduce the final docker image size. The resulting image build, as shown in the image below, reduced the size by approximately half.

![Backend Multi-Stage](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week1/save-size-multi-stage-python-backend.jpg)

```Multi-Stage Backend
FROM python:3.10-slim-buster AS compile-image

# Container
# make a new folder inside the container
WORKDIR /backend-flask

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# Outside Container -> Inside Container
# this contains the libraries we want to install to run the app
COPY requirements.txt requirements.txt

# Inside Container
# installs the python libraries used for the app
RUN pip3 install -Ur requirements.txt

FROM python:3.10-alpine AS build-image

# Set working directory
WORKDIR /backend-flask
COPY --from=compile-image /opt/venv /opt/venv

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# Outside Container -> Inside Container
# . generally means everything in the current directory
# first . is everything in the current directory ~ /backend-flask outside the container 
# second . is everything in the current directory ~ /backend-flask (WORKDIR) inside the container
COPY . .

# Set environment variables (Env Vars)
# Inside the container and will remain set when the container is running
ENV FLASK_ENV=development

EXPOSE ${PORT}

# CMD ~ Command
# this is the command you would use to run flask: python3 -m flask run --host=0.0.0.0 --port=4567
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
```

### Frontend Multi-Stage
In this example, the key difference was also using alpine to reduce the size of the final compiled image. As a result, the final size of the container was reduced by two-thirds. The number of node packages occupy a significant portion of the size, of which there are a number of extraneous packages that can be removed with an updated dependencies list, however, the current extent of work was adequate in understanding how multi-stage builds work and the resulting advantages of creating Docker images this way, which is also a best practice that turned out to be implemented in each Dockerfile. The resulting image build was approximately two-thirds less than the original build, which is shown in the below image.
*Note: In hindsight, for pruning extraneous packages from Node, an environment variable, `NODE_ENV` can be set to production, which would likely reduce some size.

![Frontend Multi-Stage](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week1/size-multi-stage-react-js-frontend.jpg)

```Multi-Stage Frontend
FROM node:16.18 AS builder-image

COPY . /frontend-react-js
WORKDIR /frontend-react-js

RUN npm install

FROM node:19-alpine AS compiler-image

COPY --from=builder-image /frontend-react-js /frontend-react-js
WORKDIR /frontend-react-js

ENV PORT=3000

EXPOSE ${PORT}

CMD ["npm", "start"]
```

## Implement a healthcheck in the V3 Docker compose file

A Health Check implementation in the Docker Compose file is necessary for ensuring that the orchestrated collection of frontend and backend containers is running without any issues. In applying this concept to the `docker-compose.yml` in the current project I learned from the following resource [Docker-Compose_Health-Check_Tutorial](https://medium.com/geekculture/how-to-successfully-implement-a-healthcheck-in-docker-compose-efced60bc08e) for documentation on how to specify the check. A curl commmand was used to test the connection to the application through to the backend_url to make sure that data is being recieved when pinging to the backend of the application.  The command is being used to make a ping to the application and return if an error is received while specifying the timing of the ping.

The Health Check was added to the frontend of the service, referencing if a connection is successful through to the backend:
```Docker-Compose Health Check
frontend-react-js:
    environment:
      REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    # Added health-check, referencing https://medium.com/geekculture/how-to-successfully-implement-a-healthcheck-in-docker-compose-efced60bc08e
    healthcheck:
      test: curl --fail "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}" || exit 1
      interval: 60s
      retries: 5
      start_period: 20s
      timeout: 10s
    volumes:
      - ./frontend-react-js:/frontend-react-js
```

## Learn how to install Docker on your localmachine and get the same containers running outside of Gitpod / Codespaces

I installed Docker on my local machine by creating an account on DockerHub and downloading the Docker Desktop application to get started. I downloaded the project folder from Github locally. In order to run the Docker Compose file locally, I needed to update the the url's for the backend and frontend to `"http://localhost:4567"` and `"http://localhost:3000"` respectively because the gitpod url's are not applicable in the local machine environment. For the frontend, I also deleted the `package-lock.json` and `package.json` files because they were interfering with the `npm install` process during `docker build`.
Once these configurations were performed, then the docker compose command was initiated to successfully orchestrate the two containers:

![Final Output of Docker Compose to Local Machine](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week1/Result%20of%20Running%20Docker%20Compose%20on%20Local%20Machine.PNG)

## Launch an EC2 instance that has docker installed, and pull a container to demonstrate you can run your own docker processes

In AWS, I launced a Linux AMI EC2 and went through the installation process of configuring the instance wtih Docker via `sudo yum install -y docker` and initiated the docker service `sudo docker service start`. Apart from pulling a container, I decided to instead build and run an image from the EC2; I decided to use the docker images from the project itself to practice in this challenge. To accomplish this task:

1. I performed a secure copy command (scp) from my local machine to EC2 to copy the project folder, as shown in the following image:
![sCP-to-EC2](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week1/scp-to-ec2.PNG)

2. After uploading the files to the EC2 instance file space, I decided to test runnning Docker with the backend, and was able to ultimately run the backend after building `docker build -t  backend-flask ./backend-flask` and running `docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask` the container, as shown in the following image:
![Running Backend Container on EC2](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week1/Running-Docker-Image-on-EC2.PNG)
