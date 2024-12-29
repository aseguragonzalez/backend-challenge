FROM mongoclient/mongoclient:latest

WORKDIR /home/app

COPY . .

ENTRYPOINT ["/bin/bash", "-c", "/home/app/rs-init.sh -h $MONGO_SERVER -d 10 -r dbrs"]
