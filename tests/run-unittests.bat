@echo off
set PYTHONPATH=../src;%PYTHONPATH%
REM Comment out backends you don't want to run
runtests.py --settings=settings_sqlite3
REM runtests.py --settings=settings_mysql
REM runtests.py --settings=settings_postgresql
REM runtests.py --settings=settings_postgresql_psycopg2 sqlevolve
