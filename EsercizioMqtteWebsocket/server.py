import asyncio
import json
import logging

import tornado.web
import tornado.websocket
import aiomqtt


BROKER = "mqtt.ssh.edu.it"   # test.mosquitto.org

clients = set()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class THandler(tornado.web.RequestHandler):
    def get(self):
        self.render("temperature.html")
        topic = "Incerti/sensor/"+"temperature"
        asyncio.create_task(mqtt_listener(topic))


class HHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("humidity.html")

        topic = "Incerti/sensor/"+"humidity"
        asyncio.create_task(mqtt_listener(topic))


class PHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pressure.html")
        topic = "Incerti/sensor/"+"pressure"
        asyncio.create_task(mqtt_listener(topic))



class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket aperto")
        clients.add(self)

    def on_close(self):
        print("WebSocket chiuso")
        clients.remove(self)


async def mqtt_listener(topic):

    logging.info("Connessione al broker MQTT...")

    async with aiomqtt.Client(BROKER) as client:
        await client.subscribe(topic)
        logging.info(f"Iscritto al topic: {topic}")

        async for message in client.messages:
            payload = message.payload.decode()
            data = json.loads(payload)
            print(data)
            ws_message = json.dumps({
                "type": "sensor",
                "data": data
            })

            # inoltro ai client WebSocket
            for c in list(clients):
                await c.write_message(ws_message)


async def main():
    logging.basicConfig(level=logging.INFO)

    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/ws", WSHandler),
            (r"/temperature.html", THandler),
            (r"/humidity.html", HHandler),
            (r"/pressure.html", PHandler),
        ],
        template_path="html",
    )

    app.listen(8888)
    print("Server Tornado avviato su http://localhost:8888")


    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
