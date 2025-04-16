# Пути
INSTALL_DIR = ./make/pywm

# Основные команды
.PHONY: all make run clean

all: make

make:  ## Установить в локальную директорию
	pip install --target=$(INSTALL_DIR) . --upgrade && rm -r ./make/bin && mv ./make/pywm/bin ./make/
clean:  ## Очистить установку
	rm -rf $(INSTALL_DIR)
