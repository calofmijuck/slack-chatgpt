docker run \
    --name mongodb \
    -d \
    -v `pwd`/data:/data/db \
    -p 27017:27017 \
    -e MONGO_INITDB_ROOT_USERNAME=root \
    -e MONGO_INITDB_ROOT_PASSWORD=root \
    mongo
