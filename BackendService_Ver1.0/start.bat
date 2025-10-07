@echo off
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting the API server...
echo The API will be available at: http://localhost:8000
echo API documentation will be available at: http://localhost:8000/docs
echo.

python main.py