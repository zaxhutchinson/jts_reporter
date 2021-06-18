del jtsreporter\jtsrep.log
pyinstaller start.py --name jtsreporter --onefile --distpath jtsreporter
copy jtsr\config.ini jtsreporter\config.ini
powershell "Compress-Archive -Force jtsreporter jtsreporter.zip"