FROM node:10 as node
WORKDIR /app
COPY package.json /app/
RUN npm install
COPY ./ /app/
RUN npm run build --prod

COPY --from=node /app/dist/angular-nginx /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf