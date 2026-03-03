# Демонстрационное приложение для автодеплоя на сервере

## Автоматическая настройка репозитория

Сделайте Fork текущего репозитория в свой GitHub и создайте `GHCR_TOKEN` в переменных окружения (информация ниже)

## Ручная настройка репозитория

Войдите в свою учётную запись GitHub и создайте ветку `production` в своём репозитории. Для этого в выпадаюшем списке с веткой `main` выберите *View all branches*. Создайте ветку с помощью кнопки *New Branch* и назовите `production`.

Вариант создания ветки `production` в терминале:
```sh
git checkout -b production
git push origin production
```

Очистите ветку `production` локально:
```sh
git fetch origin
git checkout production
git rm -r .
```

Создайте docker-compose для production:
```sh
touch docker-compose.prod.yaml
```

Выполните commit и push:
```sh
git add .
git commit -m "Clean production branch"
git push origin production --force
```

Сделайте Reset истории production:
```sh
git checkout production
git reset --hard HEAD~0
```

Защитите ветку `production`, чтобы предовтратить случайные push:
- Protect matching branch: production
- Require status checks
- Allow GitHub Actions to push

Очистить историю коммитов ветки `main`:
```sh
git checkout main
git checkout --orphan clean-main
git add -A
git commit -m "Initial commit"
git push -f origin clean-main:main
```

Очистить историю коммитов ветки `production`:
```sh
git checkout production
git checkout --orphan clean-production
git add -A
git commit -m "Initial commit"
git push -f origin clean-production:production
```

## Запуск сервиса локально

Запустите сервис локально:
```shell
docker-compose -p demo-simple-app up -d --build
```

## Запуск сервиса в продакшене

### Получение токена репозитория

Перейдите по ссылке `https://github.com/settings/tokens/new` и заполните форму создания токена:

- Введите название: `Git Access Token`
- Выбери срок действия (рекомендуется 90 дней или 1 год)
- В разделе Select scopes включите:
    - write:packages (+read:packages)
    - delete:packages
    - repo

Сохраните полученный PAT (Personal Access Token) пользователя.

Перейдите в репозиторий, выберите Settings -> Secrets and Variables -> Actions.

Нажми New Repository Secrets и вставь токен под названием `GHCR_TOKEN`

Проверьте в консоли:
```sh
echo <PAT_пользователя> | docker login ghcr.io -u <имя_пользователя> --password-stdin
```

Вы должны получить результат: `Login Succeeded`

### Развёртывание приложения репозитория

Передайте `имя_пользователя` и `PAT_пользователя` администратору сервера для настройки автодеплоя проекта вашего репозитория