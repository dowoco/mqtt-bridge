import logging
from paho.mqtt import client as mqtt_client
from flask import Flask, request

app = Flask(__name__)

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

@app.route('/send', methods=['POST'])
def processData():
    empty_values = 0

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
       try:
          result=request.get_json()
          if "client" not in result:
             app.logger.error("Missing host parameter!")
             empty_values += 1

          if "topic" not in result:
             app.logger.error("Missing key parameter!")
             empty_values += 1

          if "message" not in result:
             app.logger.error("Missing value parameter")
             empty_values += 1
       except:
             app.logger.error("Issue with parameters!")
             return 'Problem with Parameters!'

       if empty_values == 0:
          client_id = result['client']
          broker = 'xx.xx.xx.xx'
          port = 1883
          username = 'xxxxx'
          password = 'xxxxxx'
          keepalive = 60

          def connect_mqtt():
             def on_connect(client, userdata, flags, rc):
                if rc == 0:
                   app.logger.info("Connected to MQTT Broker!")
                else:
                   app.logger.error("Failed to connect, return code", rc)
             try:
                client = mqtt_client.Client(client_id)
                client.username_pw_set(username, password)
                client.on_connect = on_connect
                client.connect(broker, port)
                return client
             except:
                app.logger.error("Unable to Connect with MQTT Broker!")
                return None


          def publish(client, topic, msg):
             result = client.publish(topic, msg)
             status = result[0]

             if status == 0:
                app.logger.info(f"Send `{msg}` to topic `{topic}`")
             else:
                app.logger.error(f"Failed to send message to topic {topic}")

          client = connect_mqtt()
          if client is not None:
             client.loop_start()
             publish(client, result['topic'], result['message'])
             client.loop_stop()
             return "Data Sent!"
          else:
             app.logger.error("No Data Sent!")
             return "No Data Sent!"
       else:
          app.logger.error("Missing one or more Parameters!")
          return 'Missing Parameters!'

    else:
       app.logger.error("Content-Type not supported!")
       return 'Content-Type not supported!'
