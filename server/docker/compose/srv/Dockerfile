FROM alpine:latest

RUN apk --no-cache add python3 py3-pip git

WORKDIR /app

RUN git clone https://github.com/4rchXceed/webdash.dev.git .

WORKDIR /app/server

RUN python3 -m venv .venv
ENV PATH="/app/server/.venv/bin:$PATH"
RUN pip install -r requirements.txt

RUN chmod +x tokengen.sh start.sh
RUN ./tokengen.sh

RUN cp ./start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000

CMD ["/start.sh"]