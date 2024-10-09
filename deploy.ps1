scp -o "StrictHostKeyChecking no" -r -i c:/Users/Kang/.ssh/WebInstanceKey.pem ./project/ $env:MY_CLOUD_SERVER_HOST:~/assistant-server/

scp -o "StrictHostKeyChecking no" -r -i c:/Users/Kang/.ssh/WebInstanceKey.pem ./server/ $env:MY_CLOUD_SERVER_HOST:~/assistant-server/

# pscp -i c:/Users/Kang/.ssh/WebInstanceKey.pem ./requirements.txt $env:MY_CLOUD_SERVER_HOST:~/assistant-server/
