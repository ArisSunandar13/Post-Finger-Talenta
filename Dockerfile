FROM node:slim
WORKDIR /app
COPY . .

RUN npm install

RUN apt update -y
RUN apt install python3-pymysql -y