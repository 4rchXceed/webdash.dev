FROM alpine:latest

RUN apk --no-cache add nodejs npm git

WORKDIR /app

RUN git clone https://github.com/4rchXceed/webdash.dev.git .

WORKDIR /app/client


COPY globals.ts ./src/lib/globals.ts

RUN npm install
RUN npm run build


EXPOSE 3000

CMD ["node", "/app/client/build/index.js"]