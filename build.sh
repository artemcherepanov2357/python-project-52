#!/usr/bin/env bash
# Скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Выполняем установку, сборку статики и миграции
make setup