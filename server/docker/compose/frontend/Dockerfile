FROM alpine:latest

RUN apk --no-cache add nodejs npm git

WORKDIR /app

RUN git clone https://github.com/4rchXceed/webdash.dev.git .

WORKDIR /app/client

RUN npm install
RUN npm run build

EXPOSE 3000

RUN ["/app/client/build/index.js"]