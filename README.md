# qrcode-ui-auto

https://github.com/antfu/qrcode-toolkit

https://qrcode.antfu.me/

线程安全

# install

sudo apt-get install python3.10
cd /workspace
python3 -m venv venv
source activate
pip install -r requirements.txt
playwright install chrome

# run

pgrep -f "python3 -m src.main"
setsid bash sentinel-qrcode-ui-auto.sh &>> log/sentinel.log 2>&1 &
setsid python3 -m src.main &>> log/console.log 2>&1 &