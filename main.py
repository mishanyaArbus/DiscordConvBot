import time
from glob import glob
import curses
import sys
from disSendClass import disSendClass
import os
import logging

#logs
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename=f"logs/main_log.log",
                    format='%(asctime)s %(threadName)s: %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#end logs


def open_cfg(cfg_name):
    try:
        lines_list = [line.replace("\n","").split(", ") for line in open(cfg_name, 'r', encoding='utf-8').readlines()]
    except:
        logger.error(f"Failed to load cfg '{cfg_name}'")
        return False
    finally:
        logger.debug(f"Successfully loaded cfg '{cfg_name}'")

    msg_loc = lines_list[0]
    tokens = [lines_list[1], lines_list[2]]
    chat_id = lines_list[3]
    delay = lines_list[4]
    try:
        extra_behavior = lines_list[5]
    except:
        extra_behavior = [0]

    return [msg_loc, tokens, chat_id, *lines_list[4:]]


threads = []

cfgs = glob("*.cfg")


for cfg in cfgs:

    threads.append(disSendClass(*open_cfg(cfg), cfg_name=cfg))

    threads[len(threads) - 1].daemon = True
    threads[len(threads) - 1].name = cfg
    threads[len(threads) - 1].start()

def window_func(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

    curses.curs_set(0)
    stdscr.nodelay(True)


    info_win = curses.newwin(6, stdscr.getmaxyx()[1], 0, 0)
    main_win = curses.newwin(stdscr.getmaxyx()[0] - 8, stdscr.getmaxyx()[1], 6, 0)
    keys_win = curses.newwin(2, stdscr.getmaxyx()[1], stdscr.getmaxyx()[0] - 2, 0)

    selected_y = 0


    while True:
        info_win.clear()
        info_win.addstr(0, 0, "************DIALOG SPAM BOT************")
        info_win.addstr(1, 0, "/=====================================\\")
        info_win.addstr(2, 0, "author:  https://t.me/+VDEDg1Km_e0wYjli")
        info_win.addstr(3, 0, "join to see more good programs")
        info_win.addstr(4, 0, "\\=====================================/")
        info_win.addstr(5, 0, "-------------STATUS UPDATE-------------")
        info_win.refresh()

        keys_win.clear()
        keys_win.addstr(0, 0, "for selected: R-restart, S-stop, P-pause/unpause")
        keys_win.addstr(1,0,"arrow up and down to move between cfgs, CTRL+C to close the app, CTRL+R to add new cfgs")
        keys_win.refresh()

        key = -1

        key = stdscr.getch()

        if key == 3:
            sys.exit()

        try:
            if key == 18:
                for new_cfg in glob("*.cfg"):
                    if not new_cfg in cfgs:

                        threads.append(disSendClass(*open_cfg(new_cfg), new_cfg))

                        threads[len(threads) - 1].daemon = True
                        threads[len(threads) - 1].name = new_cfg
                        threads[len(threads)-1].start()

                        cfgs.append(new_cfg)
            elif key == curses.KEY_UP:  # arrows
                if selected_y>0:
                    selected_y = selected_y-1
            elif key == curses.KEY_DOWN:
                if selected_y<len(threads)-1:
                    selected_y = selected_y+1 # end arrows
            elif key == ord('r'):
                cfg_r  = threads[selected_y].cfg_name

                try:
                    threads[selected_y].stop()
                    threads.pop(selected_y)
                    cfgs.pop(selected_y)

                    temp_open_cfg = open_cfg(cfg_r)

                    if type(temp_open_cfg) != type(False):

                        threads.insert(selected_y, disSendClass(*temp_open_cfg, cfg_r))

                        cfgs.insert(selected_y, cfg_r)
                        threads[selected_y].daemon = True
                        threads[selected_y].name = cfg_r
                        threads[selected_y].start()
                except:
                    pass
            elif key == ord('s'):
                threads[selected_y].stopped = True
                threads.pop(selected_y)
                cfgs.pop(selected_y)
            elif key == ord('p'):
                threads[selected_y].paused = 1 - threads[selected_y].paused
        except IndexError:
            logger.error("pressed button on empty space")
        except Exception as e:
            logger.error(f"unknown error in menu {e}")

        main_win.clear()  # render

        a = 0
        for thread_d in threads:

            main_win.addstr(a, 0, thread_d.cfg_name.replace(".cfg", "") if len(thread_d.cfg_name.replace(".cfg", ""))<=14 else thread_d.cfg_name.replace(".cfg", "")[:14], curses.color_pair(selected_y==a))

            main_win.addstr(a, 15, f'{thread_d.paused*"paused"}{(not thread_d.paused)*"working"}')
            main_win.addstr(a, 25, f'{thread_d.status}')
            main_win.addstr(a, 55, f'total sent={thread_d.total_sent}')
            main_win.addstr(a, 70, f'iteration={thread_d.iteration}')

            a += 1

        main_win.refresh()

curses.wrapper(window_func)