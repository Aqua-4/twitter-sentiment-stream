#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Simplified chat demo for websockets.

Authentication, error handling, etc are left as an exercise for the reader :)
pip install websocket_client
"""

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
from websocket import create_connection
import ssl
import time
import tweepy
import asyncio


from tornado.options import define, options

define("port", default=9988, help="run on the given port", type=int)


api = tweepy.API(auth)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler), (r"/chatsocket", WSHandler)]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        myStream.filter(track=['python'], is_async=True)
        # myStream.filter(follow=["145125358"], is_async=True)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=WSHandler.cache)


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)
        WSHandler.on_message(self, {"body": status.text})


class WSHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200

    def get_socket(self):
        ws = create_connection("wss://echo.websocket.org",
                               sslopt={"cert_reqs": ssl.CERT_NONE})
        for i in range(1, 10):
            ws.send("{}--python hello {}".format(time.time(), i))
        return ws

    def get_messages(self):
        tmp_list = []
        ws = self.get_socket()
        ws.settimeout(5)
        for _ in range(10):
            tmp_list.append(ws.recv())
        ws.close()
        return tmp_list

    def get_one_msg(self):
        ws = create_connection("wss://echo.websocket.org",
                               sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.send("python hello--{}".format(time.time()))
        txt = ws.recv()
        ws.close()
        return txt

    # def get_compression_options(self):
    #     # Non-None enables compression with default options.
    #     return {}

    def open(self):
        WSHandler.waiters.add(self)

    def on_close(self):
        WSHandler.waiters.remove(self)

    # @classmethod
    # def update_cache(cls, chat):
    #     cls.cache.append(chat)
    #     if len(cls.cache) > cls.cache_size:
    #         cls.cache = cls.cache[-cls.cache_size:]

    # @classmethod
    # def send_updates(cls, chat):
    #     logging.info("sending message to %d waiters", len(cls.waiters))
    #     for waiter in cls.waiters:
    #         try:
    #             waiter.write_message(chat)
    #         except:
    #             logging.error("Error sending message", exc_info=True)

    def update_cache(self, chat):
        WSHandler.cache.append(chat)
        if len(WSHandler.cache) > WSHandler.cache_size:
            WSHandler.cache = WSHandler.cache[-WSHandler.cache_size:]

    def send_updates(self, chat):
        logging.info("sending message to %d waiters", len(WSHandler.waiters))
        for waiter in WSHandler.waiters:
            try:
                waiter.write_message(chat)
            except RuntimeError:
                asyncio.set_event_loop(asyncio.new_event_loop())
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        if(type(message) == dict):
            ws_msg = message.get("body", "")
            chat = {"id": str(uuid.uuid4()), "body": ws_msg}
            template = """<div class="message" id="m{id}">{body}</div>\n"""
            chat["html"] = template.format(id=chat['id'], body=chat['body'])
            # WSHandler.update_cache(self,chat)
        else:
            parsed = tornado.escape.json_decode(message)
            ws_msg = "{1}--{0}".format(parsed.get("body", ""),
                                       self.get_one_msg())
            chat = {"id": str(uuid.uuid4()), "body": ws_msg}
            chat["html"] = tornado.escape.to_basestring(
                self.render_string("message.html", message=chat))
        # import pdb; pdb.set_trace()
        WSHandler.update_cache(self, chat)
        WSHandler.send_updates(self, chat)


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
