FROM node:16 as node
WORKDIR /usr/local/app
# Copying specific files we actually need rather than things like node_modules.
COPY ./frontend/package.json .
COPY ./frontend/src/ ./src
COPY ./frontend/angular.json .
COPY ./frontend/tsconfig.json .
COPY ./frontend/tsconfig.app.json .
COPY ./frontend/tsconfig.spec.json .
COPY ./frontend/nginx.conf .

RUN npm install
RUN npm run build

FROM nginx:latest
COPY --from=node /usr/local/app/dist/frontend /usr/share/nginx/html
COPY ./frontend/nginx.conf /etc/nginx/nginx.conf
EXPOSE 443