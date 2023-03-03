FROM node:16.18 AS builder-image

COPY . /frontend-react-js
WORKDIR /frontend-react-js

RUN npm install
# running a build to preserve the built run to then copy over
RUN npm run build

FROM nginx:1.23-alpine AS compiler-image

ENV PORT=80

EXPOSE ${PORT}

# CMD ["npm", "start"]

# Set working directory to nginx resources directory
WORKDIR /usr/share/nginx/html
# Remove default nginx static resources
RUN rm -rf ./*
# Copies static resources from builder stage
COPY --from=builder-image /frontend-react-js/build .
# Containers run nginx with global directives and daemon off
ENTRYPOINT ["nginx", "-g", "daemon off;"]