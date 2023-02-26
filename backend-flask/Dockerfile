FROM python:3.10-slim-buster

# Container
# make a new folder inside the container
WORKDIR /backend-flask

# Outside Container -> Inside Container
# this contains the libraries we want to install to run the app
COPY requirements.txt requirements.txt

# Inside Container
# installs the python libraries used for the app
RUN pip3 install -r requirements.txt

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