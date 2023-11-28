# Переменные
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
SRC_DIR = src

# Действия по умолчанию
all: venv install test clean
# Создание виртуального окружения и установка зависимостей
venv:
	python3 -m venv $(VENV_DIR)
	$(PIP) install -r requirements.txt

# Установка модуля
install: | $(SRC_DIR)
	cd $(SRC_DIR) && ../$(PYTHON) setup.py install

# Запуск тестов
test:
	$(PYTHON) -m unittest "test_cjson.py"

# Очистка сгенерированных файлов
clean:
	rm -rf -R $(VENV_DIR)
	cd $(SRC_DIR) && rm -rf -R build dist *.egg-info

.PHONY: venv install test clean
