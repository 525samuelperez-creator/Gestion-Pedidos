import pymysql

pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()

# Bypass MySQL version check if necessary
import django.db.backends.mysql.base as mysql_base
mysql_base.DatabaseWrapper.check_database_version_supported = lambda self: None
