import threading
import requests as r
import time
from datetime import datetime
from datetime import timedelta
import logging

class disSendClass(threading.Thread):

    def set_session(self, s_token_I, s_token_II):
        self.s = [r.Session(), r.Session()]

        self.s[0].headers['authorization'] = s_token_I
        self.s[1].headers['authorization'] = s_token_II

    def set_msgfile(self, loc):
        self.msg_set: list = open(loc, 'r', encoding='utf-8').read().splitlines()

    def iterate(self):
        self.iteration += 1

        self.set_session(self.tokenss[0][self.iteration % len(self.tokenss[0])], self.tokenss[1][self.iteration % len(self.tokenss[1])])
        self.set_msgfile(self.msg_locs[self.iteration % len(self.msg_locs)])
        self.chat_id = self.chat_ids[self.iteration % len(self.chat_ids)]
        self.delay = int(self.delays[self.iteration % len(self.delays)])



    def __init__(self, tokenss, msg_locs, chat_ids, delays, extra_behavior, cfg_name, *args, **kwargs):
        super(disSendClass, self).__init__(*args, **kwargs)
        #logs
        logging.basicConfig(filename=f"logs/main_log.log",
                            format=f'%(asctime)s %(threadName)s: %(message)s',
                            filemode='w')

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        #end logs

        self.extra_behavior = int(extra_behavior)

        self.cfg_name = cfg_name

        self.paused = False
        self.stopped = False

        self.tokenss = tokenss

        self.msg_locs = msg_locs

        self.total_sent = 0
        self.msg_id = 0
        self.iteration = -1

        self.chat_ids = chat_ids
        self.delays = delays

        self.iterate()

        self.killed = False

        self.status = "initialized"
        self.resp = {}

    def run(self):
        self.status = "started"
        while not self.stopped:
            self.status = "new loop"

            self.status = "paused"
            while self.paused:
                pass

            if self.total_sent >= len(self.msg_set):
                self.iterate()

                self.msg_id = 0
                self.total_sent = 0

            msg = self.msg_set[self.total_sent]

            if self.msg_id == 0:
                _data = {'content': msg, 'tts': False}
            else:
                _data = {'content': msg, 'tts': False,
                         'message_reference': {'channel_id': self.chat_id, 'message_id': self.msg_id}}


            self.status = "trying to send request"
            while True:
                try:
                    self.resp = self.s[self.total_sent % 2].post(
                        f'https://discord.com/api/v9/channels/{self.chat_id}/messages', json=_data, timeout=2).json()
                    #self.status="wtf (for devs only)"
                except:
                    self.status = "no response"
                finally:
                    self.status = "got response"
                    break


            if 'id' in self.resp:
                self.msg_id = self.resp['id']

                self.logger.debug(self.resp)   # logging
            elif 'code' in self.resp:
                self.logger.error(self.resp)   # logging

                w_t = 3

                if self.resp['code'] == 10003:  # wrong chat_id
                    self.status = "unknown channel"

                elif self.resp['code']  ==  20016:  # rate limit
                    next_time = (datetime.now() + timedelta(seconds=self.resp['retry_after'])).strftime("%X")
                    self.status = f"waiting until {next_time}"
                    w_t=self.resp['retry_after']

                elif self.resp['code'] == 50006:  # empty msg
                    self.status = "skipping empty msg"
                    self.total_sent+=1
                    continue

                elif self.resp['code'] == 50013:  # missing access

                    if self.extra_behavior == -1:  # pause

                        self.paused = True
                        self.status = "missing access, paused"

                        while self.paused:
                            pass

                    elif self.extra_behavior > 0:  # wait

                        next_time = (datetime.now() + timedelta(seconds=self.extra_behavior)).strftime("%X")
                        self.status = f"missing access, waiting until {next_time}"
                        w_t = self.extra_behavior

                    else:  # do nothing
                        self.status = "missing access"

                elif self.resp['code'] == 50035:  # wrong msg_id
                    self.status = "no message found"
                    self.msg_id = 0

                else:   #unexpected id
                    self.status = "getting unexpected err_id"

                time.sleep(w_t)
                continue
            else:   #unexpected response
                self.logger.error(self.resp)   # logging

                if "message" in self.resp and self.resp["message"].split(":")[0]=="401":
                    self.status = "unauthorized token"
                else:
                    self.status = "getting unexpected response"
                continue

            self.total_sent += 1


            next_time = (datetime.now() + timedelta(seconds=self.delay)).strftime("%X")
            self.status = f"waiting until {next_time}"

            time.sleep(self.delay)

        self.killed = True


    def stop(self):
        self.paused = False  # Resume the thread from the suspended state, if it is already suspended
        self.stopped = True  # Set to True