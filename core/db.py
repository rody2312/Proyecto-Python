MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bdd-scc',
        'USER': 'root',
        'PASSWORD': '',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}