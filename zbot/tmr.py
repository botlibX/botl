# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0612.W0702


"timer"


import time


from objx import update
from botl import Broker, Event, Timer
from botl import find, launch, sync


from botl.parsers import NoDate, laps, today, to_day, get_day, get_hour


def init():
    for fnm, obj in find("timer"):
        if "time" not in obj:
            continue
        diff = float(obj.time) - time.time()
        if diff > 0:
            bot = Broker.first()
            evt = Event()
            update(evt, obj)
            evt.orig = object.__repr__(bot)
            timer = Timer(diff, evt.show)
            launch(timer.start)


def tmr(event):
    if not event.rest:
        nmr = 0
        for fnm, obj in find('timer'):
            if "time" not in obj:
                continue
            lap = float(obj.time) - time.time()
            if lap > 0:
                event.reply(f'{nmr} {obj.txt} {laps(lap)}')
                nmr += 1
        if not nmr:
            event.reply("no timers")
        return
    seconds = 0
    line = ""
    for word in event.args:
        if word.startswith("+"):
            try:
                seconds = int(word[1:])
            except ValueError:
                event.reply("%s is not an integer" % seconds)
                return
        else:
            line += word + " "
    if seconds:
        target = time.time() + seconds
    else:
        try:
            target = get_day(event.rest)
        except NoDate:
            target = to_day(today())
        hour =  get_hour(event.rest)
        if hour:
            target += hour
    if not target or time.time() > target:
        event.reply("already passed given time.")
        return
    event.time = target
    diff = target - time.time()
    event.reply("ok " +  laps(diff))
    event.result = []
    event.result.append(event.rest)
    timer = Timer(diff, event.show)
    update(timer, event)
    sync(timer)
    launch(timer.start)
