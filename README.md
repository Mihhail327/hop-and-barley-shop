# 🍺 Hop & Barley Shop

**Hop & Barley** — это современный интернет-магазин премиум-класса для пивоваров. Платформа предоставляет стильный интерфейс, плавную AJAX-фильтрацию каталога и полную мультиязычность для контента.

## ✨ Ключевые возможности

* **Премиум-дизайн (Glassmorphism)**: Стильный темный/светлый интерфейс с использованием полупрозрачных элементов и продвинутых CSS-транзакций.
* **Smart Catalog**: Отзывчивый каталог, использующий асинхронные JavaScript (AJAX) запросы для фильтрации, поиска с `debounce` и пагинации без перезагрузки страниц базы.
* **Мультиязычность (I18N + Modeltranslation)**: Контент сайта и база данных (модели `Product`, `Category`) полностью переведены на два языка (Русский и Английский). `django-modeltranslation` позволяет управлять переводами прямо из панели администратора.
* **Современный стек**: Использование новейшего **Django 6.0**, работа через **PostgreSQL**, управление зависимостями посредством **Poetry**.

---

## 🛠 Стек технологий

* **Backend**: Python 3.13, Django 6.0, Django Modeltranslation.
* **Frontend**: Vanilla Javascript (AJAX Fetch API), HTML5, CSS3 (CSS Variables, Flexbox, CSS Grid).
* **База данных**: PostgreSQL 15.
* **Инфраструктура**: Docker & Docker Compose.
* **Пакетный менеджер**: Poetry.

---

## 🚀 Быстрый старт (через Docker)

Проект полностью контейнеризирован и готов к запуску в несколько кликов.

### 1. Клонирование и подготовка
Убедитесь, что у вас установлены Docker и Docker Compose.
```bash
git clone <your-repository-url>
cd myshop
```

### 2. Сборка и запуск контейнеров
Сборка образа установит все зависимости через Poetry:
```bash
docker-compose up --build -d
```
Приложение будет доступно по адресу: **`http://localhost:8000`**

### 3. Применение миграций
Откройте оболочку или выполните команду снаружи для создания таблиц в PostgreSQL:
```bash
docker-compose exec web python manage.py migrate
```

### 4. Создание суперпользователя
Для входа в панель управления:
```bash
docker-compose exec web python manage.py createsuperuser
```
Панель администратора доступна по адресу: **`http://localhost:8000/shop_admin/`**

---

## 🌐 Управление переводами

Поддержка двух языков (`RU` и `EN`) интегрирована как для интерфейса, так и для базы данных.

### Обновление переводов интерфейса (.po/.mo файлы)
Файлы локализации лежат в папке `/locale`.
Если вы добавили новые `{% trans "Текст" %}` в HTML шаблоны, выполните:
```bash
# Извлечение новых фраз:
docker-compose exec web python manage.py makemigrations -a

# Компиляция переводов (необходимо применить после перевода фраз):
docker-compose exec web python manage.py compilemessages
```

### Перевод добавленных товаров (База данных)
Благодаря `django-modeltranslation` в админке Django у товаров и категорий появятся независимые поля для английского (`name_en`, `description_en`) и русского (`name_ru`, `description_ru`) языков.

Если вы добавляете поля перевода в будущем, синхронизируйте старые данные одной командой:
```bash
docker-compose exec web python manage.py update_translation_fields
```

---

## 📝 Разработка и Poetry
Если вы хотите запускать проект локально (вне Docker Container), вам потребуется **Poetry**:
```bash
# Установка зависимостей
poetry install

# Запуск локального сервера
poetry run python manage.py runserver
```

---
*© Hop & Barley Shop. Сварено с любовью 🍻*