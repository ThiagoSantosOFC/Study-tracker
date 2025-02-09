#!/bin/bash

# Cria a estrutura para a aplicação desktop
mkdir -p app/{gui,timer,charts,database,tests}

# Cria arquivos iniciais para a app desktop
touch app/__init__.py app/main.py
touch app/gui/__init__.py app/gui/main_gui.py
touch app/timer/__init__.py app/timer/timer.py
touch app/charts/__init__.py app/charts/charts.py
touch app/database/__init__.py app/database/database.py
touch app/tests/__init__.py app/tests/test_app.py

# Cria a estrutura para o backend com FastAPI
mkdir -p backend/{routers,models,database,tests/unit,tests/integration}

# Cria arquivos iniciais para o backend
touch backend/__init__.py backend/main.py
touch backend/routers/__init__.py backend/routers/sessions.py
touch backend/models/__init__.py backend/models/study.py
touch backend/database/__init__.py backend/database/connection.py
touch backend/tests/__init__.py backend/tests/unit/__init__.py backend/tests/unit/test_example.py
touch backend/tests/integration/__init__.py backend/tests/integration/test_endpoints.py

echo "Estrutura do projeto criada com sucesso!"
