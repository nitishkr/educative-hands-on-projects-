FROM node:latest
COPY . /hello-educative
RUN cd /hello-educative; npm install
EXPOSE 3000
WORKDIR /hello-educative 
ENTRYPOINT ["npm", "start"]