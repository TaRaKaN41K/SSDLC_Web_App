FROM node:20

WORKDIR /app

# Копируем зависимости отдельно для кэширования
COPY package*.json ./
RUN npm install

# Копируем весь фронтенд
COPY . .

ENV NODE_ENV=production

CMD ["npm", "run", "dev"]
