## Практическая работа 4.1. Сервис Kubernetes
### Задача
Развернуть свой собственный сервис в `Kubernetes`, по аналогии с `Практическая работа 4.1.`

**Можно использовать Minikube  Нужно развернуть сервис в связке из минимум 2 контейнеров + 1 init.
Требования:**
- минимум два `Deployment`, по количеству сервисов 
- кастомный образ для минимум одного `Deployment` (т.е. не публичный и собранный из своего `Dockerfile`)
- минимум один `Deployment` должен содержать в себе контейнер и инит-контейнер
- минимум один `Deployment` должен содержать `volume` (любой)
- обязательно использование `ConfigMap` и/или `Secret`
- обязательно `Service` хотя бы для одного из сервисов (что логично, если они работают в связке) 
- `Liveness` и/или `Readiness` пробы минимум в одном из `Deployment`
- обязательно использование лейблов (помимо обязательных `selector/matchLabel`, конечно)

### Описание
**Создание объектов через CLI**
- Разворачиваем свой собственный сервис в Kubernetes, по аналогии с `Практическая работа 4.1.`
  - минимум два Deployment, по количеству сервисов 
  - кастомный образ для минимум одного Deployment (т.е. не публичный и собранный из своего Dockerfile)
  - минимум один Deployment должен содержать в себе контейнер и инит-контейнер 
  - минимум один Deployment должен содержать volume (любой)
  - обязательно использование ConfigMap и/или Secret 
  - обязательно Service хотя бы для одного из сервисов (что логично, если они работают в связке)
  - Liveness и/или Readiness пробы минимум в одном из Deployment 
  - обязательно использование лейблов (помимо обязательных selector/matchLabel, конечно)


- **configmap.yml**
  - Используется для хранения конфигурационных данных, которые могут быть использованы контейнерами в поде. В данном случае, хранится одна переменная окружения APP_ENV, установленная в значение production.
- **Dockerfile**
  - Описывает процесс создания Docker-образа для FastAPI-приложения. Используется образ Python 3.10, устанавливаются зависимости из requirements.txt, копируются все файлы приложения, и запускается приложение с помощью Uvicorn
- **fastapi-deployment-and-service.yml**
  - Разворачивает две реплики приложения FastAPI, используя кастомный образ. Включает init-контейнер, использует ConfigMap и Secret, монтирует volume и определяет livenessProbe.
  - Создает сервис для FastAPI, который позволяет другим приложениям взаимодействовать с ним.
- **redis-deployment-and-service.yml**
  - Разворачивает одну реплику Redis.
  - Создает сервис для Redis, позволяя другим приложениям, таким как FastAPI, взаимодействовать с Redis.
- **secret.yml**
  - Используется для хранения конфиденциальных данных. В данном случае, хранится секретный ключ SECRET_KEY
- **main.py**
  - Простое приложение, которое подключается к Redis и увеличивает счетчик при каждом запросе к корневому URL (/).
___
### Запуск
```commandline
cd lab4_1
```
  
```commandline
minikube start
```
**Билдим локальный образ и загружаем его в Minikube:**
- Используется для настройки окружения командной строки Ubuntu для работы с Docker, который управляется Minikube.
```commandline
eval $(minikube docker-env)
```

```commandline
docker build -t fastapi-app:local .
```
![image](/practice/lab4_1/docs/1.png)
___
```commandline
kubectl create -f configmap.yml
kubectl create -f secret.yml
kubectl create -f fastapi-deployment-and-service.yml
kubectl create -f redis-deployment-and-service.yml
```
![image](/practice/lab4_1/docs/2.png)
![image](/practice/lab4_1/docs/4.png)
___
**OpenAPI:**
```commandline
minikube service fastapi-service --url
```
Пример:
```commandline
http://127.0.0.1:58315/docs
```
![image](https://github.com/AndreyPriv/containerization_and_orchestration_itmo/blob/main/lab4/docs/3.png)
___
```commandline
kubectl get pods
```
![image](https://github.com/AndreyPriv/containerization_and_orchestration_itmo/blob/main/lab4/docs/1.png)
___
```commandline
kubectl get configmap
kubectl get deployment
kubectl get secret
kubectl get service
```
![image](https://github.com/AndreyPriv/containerization_and_orchestration_itmo/blob/main/lab4/docs/5.png)
___
```commandline
kubectl describe pod <pod_name>
```

![image](https://github.com/AndreyPriv/containerization_and_orchestration_itmo/blob/main/lab4/docs/6.png)

___
```commandline
kubectl config view
```
![image](https://github.com/AndreyPriv/containerization_and_orchestration_itmo/blob/main/lab4/docs/7.png)
___
