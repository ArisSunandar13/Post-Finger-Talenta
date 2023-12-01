FROM node:20.10-slim
WORKDIR /app
COPY . .

RUN npm install

RUN apt update -y
RUN apt install python3-pymysql -y