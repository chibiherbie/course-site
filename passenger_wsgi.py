# -*- coding: utf-8 -*-
import sys, os
sys.path.append('/home/b/bekkerkg/flask/project/') # указываем директорию с проектом
sys.path.append('/home/b/bekkerkg/.local/lib/python3.6/site-packages') # указываем директорию с библиотеками, куда поставили Flask
from project import create_app # когда Flask стартует, он ищет application. Если не указать 'as application', сайт не заработает
application = create_app()
from werkzeug.debug import DebuggedApplication # Опционально: подключение модуля отладки
application.wsgi_app = DebuggedApplication(application.wsgi_app, True) # Опционально: включение модуля отадки
application.debug = False  # Опционально: True/False устанавливается по необходимости в отладк
