FROM alpine:latest

RUN apk --no-cache add python3 py3-pip nodejs npm git

WORKDIR /app

RUN git clone https://github.com/4rchXceed/webdash.dev.git .

WORKDIR /app/server

RUN python3 -m venv .venv
ENV PATH="/app/server/.venv/bin:$PATH"
RUN pip install -r requirements.txt

WORKDIR /app/client

RUN npm install
RUN npm run build

WORKDIR /app/server

ARG TOKEN
RUN test -n "$TOKEN" || echo "WARNING: No TOKEN provided, the server will not start!" >&2
RUN if [ -n "$TOKEN" ]; then echo "TOKEN=$TOKEN" > .env; fi

ARG ALLOWED_ORIGIN
RUN if [ -n "$ALLOWED_ORIGIN" ]; then echo "FRONTEND_URL=$ALLOWED_ORIGIN" >> .env; fi


COPY start.sh /start.sh
RUN chmod +x /start.sh

# Server port
EXPOSE 8000
# Client port
EXPOSE 9000
ENTRYPOINT ["/start.sh"]