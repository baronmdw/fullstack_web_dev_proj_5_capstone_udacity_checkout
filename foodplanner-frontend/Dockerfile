#Stage 1
FROM node:18.16.0 as node

COPY . /app
WORKDIR /app

RUN npm install
RUN npm build --prod
#Stage 2
FROM nginx:alpine
COPY --from=node /app/dist/angular-app /usr/share/nginx/html