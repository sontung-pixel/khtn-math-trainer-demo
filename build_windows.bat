@echo off
setlocal
python -m pip install --upgrade pip
python -m pip install -r requirements-build.txt
python -m PyInstaller --noconfirm --clean --onefile --windowed --name KHTN-Math-Trainer-Demo app.py
echo.
echo File da tao: dist\KHTN-Math-Trainer-Demo.exe
endlocal
