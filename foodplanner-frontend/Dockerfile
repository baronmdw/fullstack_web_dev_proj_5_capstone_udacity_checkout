#Stage 1
FROM node:18.16.0 as node

COPY . /app
WORKDIR /app

ENV url=$url
ENV apiServerUrl=$apiServerUrl
ENV audience=$audience
ENV callbackURL=$callbackURL
ENV clientId=$clientId

RUN npm install
RUN npm run build --prod
#Stage 2
FROM nginx:alpine
COPY --from=node /app/dist/foodplanner-frontend /usr/share/nginx/html