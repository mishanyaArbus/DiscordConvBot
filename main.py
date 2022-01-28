import time
from glob import glob
import curses
import sys
from disSendClass import disSendClass
import os
import logging

if not os.path.exists('logs'):
    os.makedirs('logs')

#logs
logging.basicConfig(filename=f"logs/main_log.log",
                    format='%(asctime)s %(threadName)s: %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#end logs


#first inputs
#cfg

threads = []
#threads_statuses = []
cfgs = glob("*.cfg")


for cfg in cfgs:

    lines_list = open(cfg, 'r', encoding='utf-8').read().splitlines()
    msg_loc_g = lines_list[0].split(", ")
    tokens_g = [lines_list[1].split(", "), lines_list[2].split(", ")]
    chat_id_g = lines_list[3].split(", ")
    delay_g = lines_list[4].split(", ")

    threads.append(disSendClass(tokens_g, msg_loc_g, chat_id_g, delay_g, cfg))

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
        keys_win.addstr(1,0,"arrow up and down to move between cfgs, CTRL+C to close the app, CTRL+R to add new cfgs")
        keys_win.addstr(0,0,"for selected: R-restart, S-stop, P-pause/unpause")
        keys_win.refresh()

        key = -1

        key = stdscr.getch()

        if key == 3:
            sys.exit()

        try:
            if key == 18:
                for new_cfg in glob("*.cfg"):
                    if not new_cfg in cfgs:
                        try:
                            lines_list_n = open(new_cfg, 'r', encoding='utf-8').read().splitlines()
                        except:
                            break
                        msg_loc_g_n = lines_list_n[0].split(", ")
                        tokens_g_n = [lines_list_n[1].split(", "), lines_list_n[2].split(", ")]
                        chat_id_g_n = lines_list_n[3].split(", ")
                        delay_g_n = lines_list_n[4].split(", ")

                        threads.append(disSendClass(tokens_g_n, msg_loc_g_n, chat_id_g_n, delay_g_n, new_cfg))
                        threads[len(threads) - 1].daemon = True
                        threads[len(threads) - 1].name = new_cfg
                        threads[len(threads)-1].start()

                        cfgs.append(new_cfg)
            elif key == curses.KEY_UP:  # arrows
                if selected_y>0:
                    selected_y = selected_y-1
            elif key == curses.KEY_DOWN:  # end arrows
                if selected_y<len(threads)-1:
                    selected_y = selected_y+1
            elif key == ord('r'):
                cfg_r  = threads[selected_y].cfg_name

                try:
                    lines_list_r = open(cfg_r, 'r', encoding='utf-8').read().splitlines()
                    threads[selected_y].stop()
                    threads.pop(selected_y)
                    cfgs.pop(selected_y)

                    msg_loc_r = lines_list_r[0].split(", ")
                    tokens_r = [lines_list_r[1].split(", "), lines_list_r[2].split(", ")]
                    chat_id_r = lines_list_r[3].split(", ")
                    delay_r = lines_list_r[4].split(", ")

                    threads.insert(selected_y, disSendClass(tokens_r, msg_loc_r, chat_id_r, delay_r, cfg_r))
                    cfgs.insert(selected_y, cfg_r)
                    threads[selected_y].daemon = True
                    threads[selected_y].name = cfg_r
                    threads[selected_y].start()
                except:
                    pass
            elif key == ord('s'):
                threads[selected_y].stopped = 1
                threads.pop(selected_y)
                cfgs.pop(selected_y)
            elif key == ord('p'):
                threads[selected_y].paused = 1 - threads[selected_y].paused
        except IndexError:
            logger.error("pressed button on empty space")
        except KeyboardInterrupt:
            logger.error("exiting")
            sys.exit()
        except:
            logger.error("unknown error in menu")

        main_win.clear()  # render

        a = 0
        for thread_d in threads:
            if selected_y == a:
                main_win.addstr(a, 0, thread_d.cfg_name.replace(".cfg", ""), curses.color_pair(1))
            else:
                main_win.addstr(a, 0, thread_d.cfg_name.replace(".cfg", ""), curses.color_pair(0))
            main_win.addstr(a, 15, f'{thread_d.paused*"paused"}{(not thread_d.paused)*"working"}')
            main_win.addstr(a, 25, f'{thread_d.status}')
            main_win.addstr(a, 55, f'total sent={thread_d.total_sent}')
            main_win.addstr(a, 70, f'iteration={thread_d.iteration}')
            #main_win.addstr(a, 50, f'id={thread_d.msg_id}')
            #if "message" in thread_d.resp:
                #main_win.addstr(a, 70, f'{thread_d.resp["message"]}')
            a = a + 1

        main_win.refresh()

        time.sleep(0.05)

curses.wrapper(window_func)