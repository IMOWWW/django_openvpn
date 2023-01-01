
# Django OpenVPN - Админка by IMOWWW

  

  

Юзали [Docker-Open VPN repository](https://github.com/kylemanna/docker-openvpn) раньше? Вы можете сделать создание пользователей для OpenVpn автоматически через админку Django. 


Начинаем...


# Установка проекта

Сначала установите [Docker-Open VPN](https://github.com/kylemanna/docker-openvpn) на ваш сервер и создайте пользователя. Прочитайте как [this simple tutorial in medium](https://medium.com/@gurayy/set-up-a-vpn-server-with-docker-in-5-minutes-a66184882c45).

  

После этого клонируйте этот репозиторий:

```
git clone https://github.com/IMOWWW/django_openvpn
```

Измените следующие строки в Django Settings:

```
...

# TODO: Добавьте ваш host ip сюда

ALLOWED_HOSTS = ['*']

...

# TODO: Измените username

STATICFILES_DIRS = [

BASE_DIR / "static",

'<path_to_project_dir>/django_openvpn/static/configs/',

]
```

Идем по пути users/models и изменяем следующие настройки:

```
...

# TODO: Измените путь здесь:

vpn_data_absolute_path = '<path_to_vpn_data_docker_openvpn>/vpn-data'

...

# TODO: Измените путь здесь:

output_absolute_path = "<path_to_project_dir>/static/configs/"

...
```

Создайте виртуальное окружение и активируйте:

```
cd django_openvpn

python3 -m venv venv

source venv/bin/activate
```

Установка зависимостей:

```
pip3 install -r requirements.txt
```

Мигрируете модели:

```
python3 manage.py migrate
```

Запустите сервер и войдите под следующим именем пользователя и паролем:

```
python3 manage.py runserver
```

Panel: <Server_IP>/admin/login/?next=/admin/
username: openvpn
password: openvpn

  

**Предупреждение: после входа в систему измените пароль по умолчанию.**

  
Если у вас все настройки настроены правильно, вы можете создать клиент Openvpn из раздела «Аутентификация пользователя» панели администратора. Просто имейте в виду, что вы можете подключиться к созданным конфигам без пароля, поэтому ввод правильного пароля не требуется. Это пока что единственная проблема!
  
  
  

# Скриншоты:

![Создание пользователя](https://github.com/IMOWWW/django_openvpn/blob/main/screenshots/add_user.png  "Создание пользователя")

![Изменение пользователя и Загрузка конфига](https://github.com/IMOWWW/django_openvpn/blob/main/screenshots/edit_user.png  "Изменение пользователя и Загрузка конфига")