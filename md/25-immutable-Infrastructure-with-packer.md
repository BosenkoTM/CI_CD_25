# Урок 24: Финальный проект. Создание и развертывание полнофункционального приложения

## Введение в финальный проект

В этом финальном проекте вы примените все, чему научились на протяжении курса, для создания и развертывания полнофункционального приложения с использованием Docker и Kubernetes. Этот проект будет включать создание простого веб-приложения с фронтендом и бэкендом, контейнеризацию приложения с использованием Docker и развертывание его в кластере Kubernetes. К концу этого урока вы будете иметь полное представление о том, как интегрировать все концепции, рассмотренные в курсе.

## Обзор проекта

### Архитектура приложения

Для этого проекта мы создадим простое полнофункциональное приложение, которое состоит из:

1. **Фронтенд**: приложение React, взаимодействующее с API бэкенда.
2. **Бэкенд**: приложение Node.js/Express, которое обслуживает данные во фронтенде.
3. **База данных**: база данных MongoDB для хранения данных приложения.

### Технологический стек

- **Фронтенд**: React
- **Бэкенд**: Node.js с Express
- **База данных**: MongoDB
- **Контейнеризация**: Docker
- **Оркестровка**: Kubernetes
- **Поставщик облака**: (необязательно) Развертывание на облачном поставщике, таком как AWS, GCP или Azure, или запуск локально с помощью Minikube.

## Шаг 1: Настройка структуры проекта

1. **Создайте каталог проекта**:

```bash
mkdir fullstack-app
cd fullstack-app
```

2. **Создайте подкаталоги**:

```bash
mkdir frontend backend
```

## Шаг 2: Сборка бэкенда

### 1. Создайте приложение бэкенда

1. **Перейдите в каталог бэкенда**:

```bash
cd backend
```

2. **Инициализируйте приложение Node.js**:

```bash
npm init -y
```

3. **Установите зависимости**:

```bash
npm install express mongoose cors
```

4. **Создайте файл сервера**:

Создайте файл с именем `server.js` и добавьте следующий код:

```javascript
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Подключение MongoDB
mongoose.connect('mongodb://mongo:27017/mydatabase', {
useNewUrlParser: true,
useUnifiedTopology: true,
});

const ItemSchema = new mongoose.Schema({
name: String,
});

const Item = mongoose.model('Item', ItemSchema);

app.get('/items', async (req, res) => {
const items = await Item.find();
res.json(items);
});

app.post('/items', async (req, res) => {
const newItem = new Item(req.body);
await newItem.save();
res.json(newItem);
});

app.listen(PORT, () => {
console.log(`Сервер работает на порту ${PORT}`);
});
```

5. **Создайте Dockerfile**:

Создайте файл с именем `Dockerfile` в каталоге backend со следующим содержимым:

```dockerfile
FROM node:14
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "server.js"]
```

## Шаг 3: Создание фронтенда

### 1. Создание фронтенд-приложения

1. **Перейдите в каталог фронтенда**:

```bash
cd ../frontend
```

2. **Создайте приложение React**:

Вы можете использовать Create React App для настройки фронтенда:

```bash
npx create-react-app .
```

3. **Установите Axios**:

Установите Axios для выполнения HTTP-запросов:

```bash
npm install axios
```

4. **Обновите компонент приложения**:

Замените содержимое `src/App.js` следующим кодом:

```javascript
import React, { useEffect, useState } from 'react';
импортировать axios из 'axios';

function App() {
const [items, setItems] = useState([]);
const [itemName, setItemName] = useState('');

useEffect(() => {
fetchItems();
}, []);

const fetchItems = async () => {
const response = await axios.get('http://localhost:5000/items');
setItems(response.data);
};

const addItem = async () => {
await axios.post('http://localhost:5000/items', { name: itemName });
setItemName('');
fetchItems();
};

return (
<div>
<h1>Элементы</h1>
<input
type="text"
value={itemName}
onChange={(e) => setItemName(e.target.value)}
/>
<button onClick={addItem}>Добавить элемент</button>
<ul>
{items.map((item) => (
<li key={item._id}>{item.name}</li>
))}
</ul>
</div>
);
}

export default App;
```

5. **Создайте Dockerfile**:

Создайте файл с именем `Dockerfile` в каталоге frontend со следующим содержимым:

```dockerfile
FROM node:14
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npx", "serve", "-s", "build"]
```

## Шаг 4: Создание манифестов Kubernetes

### 1. Создайте развертывание Kubernetes для MongoDB

Создайте файл с именем `mongo-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
name: mongo
spec:
replicas: 1
selector:
matchLabels:
app: mongo
template:
metadata:
labels:
app: mongo
spec:
containers:
- name: mongo
image: mongo:latest
ports:
- containerPort: 27017
---
apiVersion: v1
kind: Service
metadata:
name: mongo
spec:
ports:
- port: 27017
selector:
app: mongo
```

### 2. Создайте Развертывание Kubernetes для бэкенда

Создайте файл с именем `backend-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
name: backend
spec:
replicas: 1
selector:
matchLabels:
app: backend
template:
metadata:
labels:
app: backend
spec:
containers:
- name: backend
image: <your-dockerhub-username>/backend:latest
ports:
- containerPort: 5000
env:
- name: MONGO_URI
value: "mongodb://mongo:27017/mydatabase"
---
apiVersion: v1
kind: Service
metadata:
name: backend
spec:
ports:
- port: 5000
selector:
app: бэкенд
```

### 3. Создайте развертывание Kubernetes для фронтенда

Создайте файл с именем `frontend-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
name: frontend
spec:
replicas: 1
selector:
matchLabels:
app: frontend
template:
metadata:
labels:
app: frontend
spec:
containers:
- name: frontend
image: <your-dockerhub-username>/frontend:latest
ports:
- containerPort: 3000
---
apiVersion: v1
kind: Service
metadata:
name: frontend
spec:
ports:
- port: 3000
selector:
app: frontend
```

## Шаг 5. Создание и отправка образов Docker

1. **Создайте образы Docker**:

Перейдите в каталоги backend и frontend и соберите образы Docker:

```bash
# Для Backend
cd backend
docker build -t <your-dockerhub-username>/backend:latest .

# Для Frontend
cd ../frontend
docker build -t <your-dockerhub-username>/frontend:latest .

```

2. **Отправьте образы Docker в Docker Hub**:

```bash
docker push <your-dockerhub-username>/backend:latest
docker push <your-dockerhub-username>/frontend:latest
```

## Шаг 6: Развертывание в Kubernetes

1. **Примените развертывание MongoDB**:

```bash
kubectl apply -f mongo-deployment.yaml
```

2. **Примените развертывание бэкенда**:

```bash
kubectl apply -f backend-deployment.yaml
```

3. **Примените развертывание фронтенда**:

```bash
kubectl apply -f frontend-deployment.yaml
```

## Шаг 7: Доступ к приложению

1. **Получить URL-адрес службы фронтенда**:

Если вы используете Minikube, вы можете получить доступ к службе фронтенда с помощью:

```bash
 minikube service frontend
```

Если вы используете облако, может потребоваться настроить Ingress или использовать тип службы LoadBalancer для доступа к фронтенду.

2. **Протестируйте приложение**:

Откройте веб-браузер и перейдите по URL-адресу, предоставленному предыдущей командой. Вы должны иметь возможность добавлять элементы в список и видеть их отображение.

## Заключение

В этом уроке вы создали и развернули полнофункциональное приложение с использованием Docker и Kubernetes. Вы создали фронтенд React, бэкенд Node.js и базу данных MongoDB, контейнеризировали каждый компонент и развернули их в кластере Kubernetes. Этот проект демонстрирует, как интегрировать концепции, изученные в ходе курса, и обеспечивает основу для создания более сложных приложений в будущем. На следующем уроке мы обобщим основные концепции, рассмотренные в ходе курса, и обсудим следующие шаги для дальнейшего обучения и изучения.

