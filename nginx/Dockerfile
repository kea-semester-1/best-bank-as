FROM nginx:alpine

RUN apk update
RUN apk add certbot certbot-nginx

RUN mkdir /etc/letsencrypt
COPY entrypoint.sh .
COPY scheduler.txt .

ENTRYPOINT ["sh", "entrypoint.sh"]
