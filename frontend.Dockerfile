# Stage 1: Compile and Build angular codebase
# Use official node image as the base image
FROM node:16 as build
# Set the working directory
WORKDIR /usr/local/app
# Add the source code to app
COPY ./frontend/ /usr/local/app/
# Install all the dependencies
RUN npm install
# Generate the build of the application
RUN npm run build

FROM nginx:latest
# Copy the build output to replace the default nginx contents.
COPY --from=build /usr/local/app/dist/frontend /usr/share/nginx/html
# Expose port 80 maybe 443 in the future
EXPOSE 80