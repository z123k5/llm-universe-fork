scp -o "StrictHostKeyChecking no" -r -i c:/Users/Kang/.ssh/WebInstanceKey.pem ./project/ ./server/ requirements.txt %MY_CLOUD_SERVER_HOST%:~/assistant-server/