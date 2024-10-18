cd /home/git/assistant-server.git/
cd server
nohup python serve.py &
cd airport
nohup python serve_airport.py &
cd ../../project/myserve
nohup python pchatassistant_serve.py &
