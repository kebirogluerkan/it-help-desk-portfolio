@echo off
setlocal

python src\generate_data.py || exit /b 1
python src\quality_check.py || exit /b 1
python src\load_database.py || exit /b 1
python src\analyze.py || exit /b 1
python -m unittest discover -s tests -v || exit /b 1

echo.
echo Project completed successfully.
