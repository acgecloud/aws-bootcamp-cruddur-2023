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