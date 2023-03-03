#!/bin/bash
# runs the starting frontend task
# Enter the appropriate tag name for running this script
docker run --rm -it -p 3000:3000 -d frontend-react-js:$1 npm start
# Latest multi-build stage docker command:
# docker run --rm -it -p 80:80 -d frontend-react-js:$1 nginx -g daemon off;