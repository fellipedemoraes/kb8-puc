FROM node:20-alpine3.19 AS build

WORKDIR /app

COPY package*.json .

RUN npm ci

COPY . .

ENV REACT_APP_BACKEND_URL api

RUN npm run build

FROM nginx:1.27.2-alpine

COPY --from=build /app/.nginx/default.conf /etc/nginx/conf.d/default.conf

WORKDIR /usr/share/nginx/html

RUN rm -rf ./*

COPY --from=build /app/build .

ENTRYPOINT ["nginx", "-g", "daemon off;"]