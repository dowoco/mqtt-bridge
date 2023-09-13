image_name=dowoco/mqtt-bridge
app_name=mqtt-bridge

build:
        docker build -t $(image_name) .

run:
        docker run --detach -p 5000:5000 --name="$(app_name)" $(image_name)

kill:
        @echo 'Killing container...'
        docker stop $(app_name)
        docker rm $(app_name)
