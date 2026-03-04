# Демонстрационное приложение для автодеплоя на сервере с Coolify

## Запуск сервиса локально

Запустите сервис локально:
```shell
docker-compose -p demo-app-coolify up -d --build
```

## Настройка сервера

### Настройка администратора

Администратор должен в своей учётной записи перейти в меню `Teams` и открыть вкладку `Members`. В блоке `Invite New Member` нужно заполнить поле `Email` (ваша электронная почта), выбрать `Role` (`Member`) и нажать `Generate Invintation Link`. Запросите полученную пригласительную ссылку.

После перехода по пригласительной ссылке от администратора установите новый пароль, войдите в свою учётную запись, перейдите в указаннную Team (например, `students`) по начните настройку

### Создание Private Key

Перейдите в меню `Keys & Tokens`, откройте вкладку `Private Keys` и нажмите `Add`. В появившемся модальном окне укажите название и описание ключа и нажмите `Generate new ED25519 SSH Key`. Скопируйте сгенерированный `Public Key` и нажмите `Continue`.

В своём приватном репозитории проекта перейдите в `Settings -> Deploy keys` и нажмите `Add deploy key`. Введите название ключа, например `Coolify`, вставьте скопированный ранее `Public Key` и нажмите `Add key`

Попросите администратора добавить скопированный `Public Key` на сервер по SSH:
```sh
nano /root/.ssh/authorized_keys
```

### Добавление сервера

Для создания сервера необходимо над главным меню переключиться на общую Team или выбрать свою, перейти в меню `Servers` и нажать на кнопку `Add`. В модальном окне создания сервера нужно указать Name (`localhost`), IP Address/Domain (`host.docker.internal`), `Port` (`22`), User (`root`), выбрать `Private Key`, созданный ранее, и нажать `Continue`

Когда сервер в Coolify создан и ключи добавлены администратором в `authorized_keys`, нужно его открыть и валидировать, нажав на `Validate Server & Install Docker Engine`

### Создание токена API

API Token необходим для отправки авторизированных запросов на сервер с Coolify в рамках деплоя (например, триггера деплоя новой сборки из GitHub Actions)

Перейдите в меню `Keys & Tokens` и откройте вкладку `API Tokens`. Укажите название создаваемого токена и выберите разрешения `write`, `deploy`, `read`. Нажмите `Create` и скопируйте сгенерированный токен *без первой цифры и следующей вертикальной черты*.

В своём репозитории проекта перейдите в `Settings -> Secrets & Variables -> Actions` и нажмите `New Repository Secret`. Укажите название `COOLIFY_TOKEN` и вставьте скопированный токен в поле `Secret`. Сохраните, нажав на кнопку `Add Secret`

### Создание проекта

Перейдите в меню `Projects` и нажмите `Add`. Введите название и описание проекта и нажмите `Continue`. На следующей странице `Resources` нажмите `Add Resource` и выберите `Public Repository`, если ваш проект находится в публичном репозитория GitHub, или `Private Repository`, если ваш проект находится в приватном репозитории. Затем выберите `private key`: вам будет предложен ключ команды `student` для подключения к серверу `localhost`. В окне создания приложения укажите:
- Repository URL: адрес вашего репозитория на GitHub (например, `git@github.com:aleksioprime/demo-app-coolify.git`)
- Branch: ветку вашего репозитория (например, `main`)
- Build Pack: способ сборки приложения (например, `Docker Compose`)
- Base Directory: основной каталог (например, `/` или оставить по-умолчанию)
- Docker Compose Location: путь к файлу docker-compose.yaml (например, `/docker-compose.prod.yaml`)

После создания ресурса (приложения) должен загрузиться указанный в настройках файл Docker Compose (значит, доступ к репозиторию и файлу сборки есть)

Перейдите на вкладке `Configuration` в меню `Advanced` и выберите `Raw Compose Deployment` для запуска сборки чистого Docker Compose без дополнительных настроек Coolify

Перейдите на вкладке `Configuration` в меню `Environment Variables` и добавьте переменную `IMAGE_TAG` с начальным значением `latest`. В дальнейшем она будет перезаписываться во время сборки в GitHub Actions

Перейдите на вкладке `Configuration` в меню `Webhooks` и скопируйте два фрагмента строки `Deploy Webhook` (например, `https://coolify.technocrew.ru/api/v1/deploy?uuid=ygw8skswo448gs440skwcssw&force=false`): основной домен (например, `https://coolify.technocrew.ru`) и UUID приложения (например, `ygw8skswo448gs440skwcssw`)

В своём репозитории проекта перейдите в `Settings -> Secrets & Variables -> Actions` и добавьте переменные. В переменную с названием `COOLIFY_API` вставьте основной домен (например, `https://coolify.technocrew.ru`),  а в переменную `COOLIFY_APP` вставьте UUID приложения (например, `ygw8skswo448gs440skwcssw`)

## Настройка репозитория

### Создание токена GHCR

Перейдите по ссылке `https://github.com/settings/tokens/new` и заполните форму создания токена:

- Введите название: `Git Access Token`
- Выбери срок действия (рекомендуется 90 дней или 1 год)
- В разделе Select scopes включите:
    - write:packages (+read:packages)
    - delete:packages
    - repo

Скопируйте полученный PAT (Personal Access Token) пользователя.

Перейдите в свой репозиторий, выберите `Settings -> Secrets and Variables -> Actions`. Нажми New Repository Secrets и вставьте токен под названием `GHCR_TOKEN`

### Создание Secrets

Перейдите своём репозитории в `Settings -> Secrets and Variables -> Actions` и проверьте созданные переменные:

- `GHCR_TOKEN` - PAT (Personal Access Token) пользователя
- `COOLIFY_TOKEN` - API Token из Coolify (`Keys & Tokens` -> `API Tokens`)
- `COOLIFY_API` - основной домен ресурса Coolify (можно посмотреть в ссылке WebHook приложения)
- `COOLIFY_APP` - UUID приложения Coolify (можно посмотреть в ссылке WebHook приложения)

### Добавление ключа деплоя

Перейдите в своём репозитории `Settings -> Deploy keys` и нажмите `Add deploy key`. Введите название ключа, например `Coolify`, вставьте скопированный ранее `Public Key` из Coolify и нажмите `Add key`

### Изменение публичности сборки ghcr.io

Перейдите в свой GitHub, выберите вкладку `Packages` (например, `https://github.com/aleksioprime?tab=packages`) и откройте нужный образ (например, `demo-app-coolify`). Откройте настройки `Package settings` в правом колонке страницы, перейдите в самый низ к блоку `Danger Zone` и нажмите `Change visibility`. Выберите `Public`, введите для подтверждения название сборки (например, `demo-app-coolify`) и нажмите `I understand the consequences, change package visibility`

### Работа с приватной сборкой ghcr.io

Если нужно работать с приватной сборкой, то необходимо добавить ваш PAT (Personal Access Token) пользователя на сервер через `docker login`

Перейдите в root:
```sh
sudo -i
```
Выполните авторизацию в Docker:
```sh
echo "<ваш_ghcr_токен>" | docker login ghcr.io -u <пользователь_github> --password-stdin
```
Проверьте файл:
```sh
cat /root/.docker/config.json
```

Текущий пользователь в системе может иметь только один ghcr токен. При добавлении нового старый заменяется