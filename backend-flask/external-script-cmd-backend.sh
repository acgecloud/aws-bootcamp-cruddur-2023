#!/bin/bash
# runs the starting backend task
# Enter the appropriate tag name for running this script
docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask:$1 python3 -m flask run --host=0.0.0.0 --port=4567