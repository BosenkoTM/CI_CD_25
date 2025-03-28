##  Сервис Kubernetes 1 часть. (Практические работы 3.2, 4.1.)
### Задача
Развернуть свой собственный сервис в `Kubernetes`

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
- Разворачиваем свой собственный сервис в Kubernetes
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

### Установка minikube.
```commandline
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
```

```commandline
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### Добавление пользователя в группу Docker.
```commandline
sudo usermod -aG docker $USER && newgrp docker
```

### Установка kubectl.
kubectl — это командный инструмент для управления кластерами Kubernetes. 

```commandline
sudo snap install kubectl --classic
```

___
### Запуск

```commandline
cd lab4_1
```
  
```commandline
minikube start --memory=2048mb --driver=docker 
```
![image](https://github.com/BosenkoTM/CI_CD_25/blob/main/practice/lab4_1/docs/1.png)
**Билдим локальный образ и загружаем его в Minikube:**
- Используется для настройки окружения командной строки Ubuntu для работы с Docker, который управляется Minikube.
```commandline
eval $(minikube docker-env)
```

```commandline
docker build -t fastapi-app:local .
```

```commandline
kubectl create -f configmap.yml
kubectl create -f secret.yml
kubectl create -f fastapi-deployment-and-service.yml
kubectl create -f redis-deployment-and-service.yml
```

![image](/practice/lab4_1/docs/2.png)
___


![image](/practice/lab4_1/docs/4.png)
___
**OpenAPI:**
```commandline
minikube service fastapi-service --url
```
Пример:
```commandline
http://192.168.49.2:30001/docs
```

![image](/practice/lab4_1/docs/33.png)
___
```commandline
kubectl get pods
```

![image](/practice/lab4_1/docs/55.png)

___
```commandline
kubectl describe pod <pod_name>
```

![image](/practice/lab4_1/docs/66.png)

___

```commandline
kubectl get services
```


```commandline
kubectl config view
```
![image](/practice/lab4_1/docs/77.png)
___



| Вариант | Задание 1 | Задание 2 | Задание 3 | Задание 4 |
| --- | --- | --- | --- | --- |
| **Вариант 1. Kubernetes. Часть 1 (redis)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **redis**. Измените файл: <br> – Запуск без пароля (замените переменную на <code>ALLOW_EMPTY_PASSWORD=yes</code>). <br> – Фиксируйте образ на версии **6.0.13**. <br> – Добавьте Service для доступа. <br> Приложите итоговый файл. | Напишите команды kubectl для контейнера из предыдущего задания: <br> – Выполнить внутри контейнера команду <code>ps aux</code>;<br> – Просмотреть логи за последние 5 минут;<br> – Удалить контейнер;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с конфигурацией nginx (произвольная настройка); <br> – Deployment, использующий ConfigMap; <br> – Ingress, направляющий запросы по пути <code>/test</code> на сервис. Приложите итоговый файл. |
| **Вариант 2. Kubernetes. Часть 1 (nginx)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и пришлите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **nginx**. Измените файл: <br> – Добавьте аргумент для запуска с кастомной конфигурацией;<br> – Фиксируйте образ на версии **1.19.0**;<br> – Добавьте Service для доступа. <br> Приложите итоговый файл. | Напишите команды kubectl для контейнера: <br> – Выполнить <code>ps aux</code> внутри контейнера;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт локальной машины для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **nginx** (например, изменить приветственное сообщение);<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/custom</code> на сервис. Приложите итоговый файл. |
| **Вариант 3. Kubernetes. Часть 1 (postgres)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров, приложив скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **postgres**. Измените файл: <br> – Запустите без пароля (уберите переменную пароля);<br> – Фиксируйте образ на версии **13.0**;<br> – Добавьте Service для доступа к базе. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить контейнер;<br> – Пробросить локальный порт для отладки. | Доп. задание*: Напишите YAML для: <br> – ConfigMap с кастомной конфигурацией для **postgres** (например, параметры конфигурации базы);<br> – Deployment с подключением ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/db</code> на сервис. |
| **Вариант 4. Kubernetes. Часть 1 (rabbitmq)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров, приложив скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **rabbitmq**. Измените файл: <br> – Настройте запуск без обязательной аутентификации;<br> – Фиксируйте образ на версии **3.8.0**;<br> – Добавьте Service для доступа к очередям. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить внутри контейнера команду <code>ps aux</code>;<br> – Просмотреть логи за последние 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с кастомными настройками для **rabbitmq**;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/mq</code> на сервис. |
| **Вариант 5. Kubernetes. Часть 1 (mongo)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **mongo**. Измените файл: <br> – Запустите без пароля (уберите переменную аутентификации);<br> – Фиксируйте образ на версии **4.2**;<br> – Добавьте Service для доступа к базе. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить <code>ps aux</code> внутри контейнера;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **mongo** (например, параметры репликации);<br> – Deployment с подключением ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/db</code> на сервис. |
| **Вариант 6. Kubernetes. Часть 1 (elasticsearch)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и пришлите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **elasticsearch**. Измените файл: <br> – Отключите базовую аутентификацию;<br> – Фиксируйте образ на версии **7.10.0**;<br> – Добавьте Service для доступа к кластеру. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить внутри контейнера команду <code>ps aux</code>;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **elasticsearch**;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/search</code> на сервис. |
| **Вариант 7. Kubernetes. Часть 1 (redis v6.2.5)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **redis**. Измените файл: <br> – Запуск без пароля (<code>ALLOW_EMPTY_PASSWORD=yes</code>);<br> – Фиксируйте образ на версии **6.2.5**;<br> – Добавьте Service для доступа. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить локальный порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **redis** (например, параметры кэширования);<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/cache</code> на сервис. |
| **Вариант 8. Kubernetes. Часть 1 (nginx v1.21.0)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **nginx**. Измените файл: <br> – Добавьте кастомные параметры запуска;<br> – Фиксируйте образ на версии **1.21.0**;<br> – Добавьте Service для доступа. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить внутри контейнера команду <code>ps aux</code>;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **nginx** (например, изменение стандартного порта);<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/site</code> на сервис. |
| **Вариант 9. Kubernetes. Часть 1 (memcached)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **memcached**. Измените файл: <br> – Убедитесь, что контейнер запускается без пароля;<br> – Фиксируйте образ на версии **1.6**;<br> – Добавьте Service для доступа к кэшу. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри контейнера;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить локальный порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **memcached**;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/cache</code> на сервис. |
| **Вариант 10. Kubernetes. Часть 1 (wordpress)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **wordpress**. Измените файл: <br> – Убедитесь, что приложение запускается без обязательного пароля;<br> – Фиксируйте образ на версии **5.7**;<br> – Добавьте Service для доступа к сайту. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **wordpress** (например, параметры темы);<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/blog</code> на сервис. |
| **Вариант 11. Kubernetes. Часть 1 (phpMyAdmin)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **phpMyAdmin**. Измените файл: <br> – Настройте запуск без пароля;<br> – Фиксируйте образ на версии **5.1**;<br> – Добавьте Service для доступа к интерфейсу. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **phpMyAdmin**;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/admin</code> на сервис. |
| **Вариант 12. Kubernetes. Часть 1 (Jenkins)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **Jenkins**. Измените файл: <br> – Настройте запуск без пароля (или с дефолтными настройками);<br> – Фиксируйте образ на версии **2.319**;<br> – Добавьте Service для доступа к веб-интерфейсу. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **Jenkins** (например, параметры сборки);<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/ci</code> на сервис. |
| **Вариант 13. Kubernetes. Часть 1 (Prometheus)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **Prometheus**. Измените файл: <br> – Настройте запуск без пароля;<br> – Фиксируйте образ на версии **2.30**;<br> – Добавьте Service для доступа к метрикам. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **Prometheus** (например, scrape-конфигурация);<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/metrics</code> на сервис. |
| **Вариант 14. Kubernetes. Часть 1 (Grafana)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **Grafana**. Измените файл: <br> – Запустите без пароля (используйте дефолтную конфигурацию);<br> – Фиксируйте образ на версии **8.0**;<br> – Добавьте Service для доступа к дашбордам. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **Grafana**;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/graf</code> на сервис. |
| **Вариант 15. Kubernetes. Часть 1 (Keycloak)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **Keycloak**. Измените файл: <br> – Запустите без обязательного пароля;<br> – Фиксируйте образ на версии **15.0**;<br> – Добавьте Service для доступа к консоли. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **Keycloak** (например, realm-конфигурация);<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/auth</code> на сервис. |
| **Вариант 16. Kubernetes. Часть 1 (Consul)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров, приложив скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **Consul**. Измените файл: <br> – Настройте запуск без пароля;<br> – Фиксируйте образ на версии **1.9**;<br> – Добавьте Service для доступа к кластеру. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **Consul**;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/consul</code> на сервис. |
| **Вариант 17. Kubernetes. Часть 1 (etcd)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров, приложив скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **etcd**. Измените файл: <br> – Запустите без пароля;<br> – Фиксируйте образ на версии **3.4**;<br> – Добавьте Service для доступа к хранилищу ключ-значение. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **etcd**;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/etcd</code> на сервис. |
| **Вариант 18. Kubernetes. Часть 1 (Cassandra)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров, приложив скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **Cassandra**. Измените файл: <br> – Запустите без пароля;<br> – Фиксируйте образ на версии **3.11**;<br> – Добавьте Service для доступа к базе данных. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **Cassandra**;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/cdb</code> на сервис. |
| **Вариант 19. Kubernetes. Часть 1 (Kafka)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров, приложив скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **Kafka**. Измените файл: <br> – Запустите без пароля;<br> – Фиксируйте образ на версии **2.7**;<br> – Добавьте Service для доступа к брокеру сообщений. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **Kafka**;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/kafka</code> на сервис. |
| **Вариант 20. Kubernetes. Часть 1 (Zookeeper)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров, приложив скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **Zookeeper**. Измените файл: <br> – Запустите без пароля;<br> – Фиксируйте образ на версии **3.6**;<br> – Добавьте Service для доступа к сервису координации. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **Zookeeper**;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/zk</code> на сервис. |
| **Вариант 21. Kubernetes. Часть 1 (nginx v1.20.0)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **nginx**. Измените файл: <br> – Добавьте пользовательский конфигурационный аргумент;<br> – Фиксируйте образ на версии **1.20.0**;<br> – Добавьте Service для доступа к веб-серверу. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **nginx** (например, измените индексную страницу);<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/web</code> на сервис. |
| **Вариант 22. Kubernetes. Часть 1 (redis с репликой)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **redis**. Измените файл: <br> – Запуск без пароля (<code>ALLOW_EMPTY_PASSWORD=yes</code>);<br> – Фиксируйте образ на версии **6.0.15**;<br> – Установите <code>replicas: 2</code>;<br> – Добавьте Service для доступа. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить локальный порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **redis**;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/cache</code> на сервис. |
| **Вариант 23. Kubernetes. Часть 1 (postgres с PV)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров, приложив скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **postgres**. Измените файл: <br> – Запуск без пароля;<br> – Фиксируйте образ на версии **12.5**;<br> – Добавьте PersistentVolumeClaim для хранения данных;<br> – Добавьте Service для доступа к базе. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **postgres** (например, параметры репликации);<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/db</code> на сервис. |
| **Вариант 24. Kubernetes. Часть 1 (MySQL)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **MySQL**. Измените файл: <br> – Запустите без пароля;<br> – Фиксируйте образ на версии **8.0**;<br> – Добавьте Service для доступа к базе данных. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **MySQL**;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/mysql</code> на сервис. |
| **Вариант 25. Kubernetes. Часть 1 (MariaDB)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров, приложив скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **MariaDB**. Измените файл: <br> – Запустите без пароля;<br> – Фиксируйте образ на версии **10.5**;<br> – Добавьте Service для доступа к базе. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **MariaDB**;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/mariadb</code> на сервис. |
| **Вариант 26. Kubernetes. Часть 1 (Node.js)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **Node.js** приложения. Измените файл: <br> – Убедитесь, что приложение запускается без пароля;<br> – Фиксируйте образ на версии **14**;<br> – Добавьте Service для доступа к приложению. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для вашего **Node.js** приложения;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/app</code> на сервис. |
| **Вариант 27. Kubernetes. Часть 1 (Python-Flask)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **Python-Flask** приложения. Измените файл: <br> – Запустите без пароля;<br> – Фиксируйте образ на версии **3.9**;<br> – Добавьте Service для доступа к API. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **Flask** приложения;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/api</code> на сервис. |
| **Вариант 28. Kubernetes. Часть 1 (Java-App)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **Java** приложения. Измените файл: <br> – Запустите без пароля;<br> – Фиксируйте образ на версии **11**;<br> – Добавьте Service для доступа к приложению. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **Java** приложения;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/java</code> на сервис. |
| **Вариант 29. Kubernetes. Часть 1 (Go-App)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **Go** приложения. Измените файл: <br> – Запустите без пароля;<br> – Фиксируйте образ на версии **1.16**;<br> – Добавьте Service для доступа к приложению. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **Go** приложения;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/go</code> на сервис. |
| **Вариант 30. Kubernetes. Часть 1 (Ruby-App)** | Запустите Kubernetes локально (k3s или minikube). Проверьте работу системных контейнеров и приложите скриншот команды: <code>kubectl get po -n kube-system</code>. | Имеется YAML с деплоем для **Ruby** приложения. Измените файл: <br> – Запустите без пароля;<br> – Фиксируйте образ на версии **2.7**;<br> – Добавьте Service для доступа к приложению. <br> Приложите итоговый YAML. | Напишите команды kubectl для контейнера: <br> – Выполнить команду <code>ps aux</code> внутри pod;<br> – Просмотреть логи за 5 минут;<br> – Удалить pod;<br> – Пробросить порт для отладки. | Доп. задание*: Создайте YAML для: <br> – ConfigMap с настройками для **Ruby** приложения;<br> – Deployment, использующий ConfigMap;<br> – Ingress, направляющий запросы по пути <code>/ruby</code> на сервис. |



# Пример выполнения «Kubernetes. Часть 1»

---

### Задание 1

**Выполните действия:**

1. Запустите Kubernetes локально, используя k3s или minikube на свой выбор.
1. Добейтесь стабильной работы всех системных контейнеров.
2. В качестве ответа пришлите скриншот результата выполнения команды 

```bash
kubectl get po -n kube-system.
```



------
### Задание 2


Есть файл с деплоем:

```
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
spec:
  selector:
    matchLabels:
      app: redis
  replicas: 1
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: master
        image: bitnami/redis
        env:
         - name: REDIS_PASSWORD
           value: password123
        ports:
        - containerPort: 6379
```

------
**Выполните действия:**

1. Измените файл с учётом условий:

 * redis должен запускаться без пароля;
 * создайте Service, который будет направлять трафик на этот Deployment;
 * версия образа redis должна быть зафиксирована на 6.0.13.

2. Запустите Deployment в своём кластере и добейтесь его стабильной работы.
3. В качестве решения пришлите получившийся файл.

#### Ответ:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
spec:
  selector:
    matchLabels:
      app: redis
  replicas: 1
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: master
        image: bitnami/redis:6.0.13
        env:
         - name: ALLOW_EMPTY_PASSWORD
           value: "yes"
        ports:
         - containerPort: 6379
```

```
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
    - protocol: TCP
      port: 6379
      targetPort: 6379
```

##### Скриншот:



------
### Задание 3

**Выполните действия:**

1. Напишите команды kubectl для контейнера из предыдущего задания:

 - выполнения команды ps aux внутри контейнера;
 - просмотра логов контейнера за последние 5 минут;
 - удаления контейнера;
 - проброса порта локальной машины в контейнер для отладки.

2. В качестве решения пришлите получившиеся команды.

#### Команты:
sudo kubectl exec redis-7bfccd74cd-8bhrk -- ps aux

sudo kubectl logs --since=5m redis-7bfccd74cd-8bhrk

sudo kubectl delete -f redis.yaml && sudo kubectl delete -f redis-service.yaml

sudo kubectl port-forward redis-7bfccd74cd-jpg8j 12345:6739

#### Скриншот:




------
## Дополнительные задания* (со звёздочкой)

Их выполнение необязательное и не влияет на получение зачёта по домашнему заданию. Можете их решить, если хотите лучше разобраться в материале.

---

### Задание 4*

Есть конфигурация nginx:

```
location / {
    add_header Content-Type text/plain;
    return 200 'Hello from k8s';
}
```

**Выполните действия:**

1. Напишите yaml-файлы для развёртки nginx, в которых будут присутствовать:

 - ConfigMap с конфигом nginx;
 - Deployment, который бы подключал этот configmap;
 - Ingress, который будет направлять запросы по префиксу /test на наш сервис.

2. В качестве решения пришлите получившийся файл.

#### .yaml:

configmap.yaml
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-configmap
data:
  nginx.conf: |
    location / {
      add_header Content-Type text/plain;
      return 200 'Hello from k9s';
    }
```
---
deploument.yaml
```
kind: deployment
metadata:
 name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
          ports:
            - containerPort: 80
          volumeMounts:
            - name: nginx-config
              mountPath: /etc/nginx/nginx.conf
              subPath: nginx.conf
      volumes:
        - name: nginx-config
          configMap:
            name: nginx-configmap
```
---
ingress.yaml
```
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: nginx-ingress
spec:
  rules:
    - http:
        paths:
          - path: /test
            backend:
              serviceName: nginx-service
              servicePort: 80
```


















