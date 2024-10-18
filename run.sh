cd /home/git/assistant-server.git/
cd server
nohup python serve_airport.py &
nohup python serve.py &
cd ../project/myserve
nohup python pchatassistant_serve.py &
