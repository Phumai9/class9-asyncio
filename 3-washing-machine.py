import time
import random
import json
import asyncio
import aiomqtt
from enum import Enum
import sys
import os

student_id = "6310301009"

# State 
S_OFF       = 'OFF'
S_READY     = 'READY'
S_FAULT     = 'FAULT'
S_FILLWATER = 'FILLWATER'
S_HEATWATER = 'HEATWATER'
S_WASH      = 'WASH'
S_RINSE     = 'RINSE'
S_SPIN      = 'SPIN'
S_STOP      = 'STOP'

# Function
S_DOORCLOSED            = 'DOORCLOSE'
S_FULLLEVELDETECTED     = 'FULLLEVELDETECTED'
S_TEMPERATUREREACHED    = 'TEMPERATUREREACHED'
S_FUNCTIONCOMPLETED     = 'FUNCTIONCOMPLETED'
S_TIMEOUT               = 'TIMEOUT'
S_MOTORFAILURE          = 'MOTORFAILURE'
S_FAULTCLEARED          = 'FAULTCLEARED'

class MachineStatus():
    def __init__(self):
        pressure = round(random.uniform(2000,3000), 2)
        temperature = round(random.uniform(25.0,40.0), 2)

class MachineMaintStatus():
    def __init__(self) -> None:
        self.filter = random.choice(["clear", "clogged"])
        self.noise = random.choice(["quiet", "noisy"])

class WashingMachine:
    def __init__(self, serial):
        self.MACHINE_STATUS = 'OFF'
        self.SERIAL = serial
        self.task = None
        self.event = asyncio.Event()

async def waiting(w, nextstate, status_type):
    try:
        print(f'{time.ctime()} - Now waiting for {w.MACHINE_STATUS}')
        await asyncio.sleep(10)
        print(f'{time.ctime()} - Waiting 10 second already! > Time out <')
        w.MACHINE_STATUS = nextstate
        w.FAULT_TYPE = status_type
        print(f'{time.ctime()} - [{w.SERIAL}] STATUS : {w.MACHINE_STATUS}')
    except asyncio.CancelledError:
        print(f'{time.ctime()} - Waiting function is canceled!')

async def waiting_to_nextstate(w, event):
    print(f"{time.ctime()} - [{w.SERIAL}-{w.MACHINE_STATUS}] Waiting next state...")
    await event.wait()
    print(f"{time.ctime()} - [{w.SERIAL}-{w.MACHINE_STATUS}] ... got it")

async def MachineRestart(w, event):
    print(f"{time.ctime()} - [{w.SERIAL}-{w.MACHINE_STATUS}] New starting wait for a next state...")
    await event.wait()

async def publish_message(w, client, app, action, name, value):
    print(f"{time.ctime()} - [{w.SERIAL}] {name} : {value}")
    await asyncio.sleep(2)
    payload = {
                "action"    : "get",
                "project"   : student_id,
                "model"     : "model-01",
                "serial"    : w.SERIAL,
                "name"      : name,
                "value"     : value
            }
    print(f"{time.ctime()} - PUBLISH - [{w.SERIAL}] - {payload['name']} > {payload['value']}")
    await client.publish(f"v1cdti/{app}/{action}/{student_id}/model-01/{w.SERIAL}", payload=json.dumps(payload))

async def CoroWashingMachine(w, client):

    while True:
        w.event = asyncio.Event()
        waiter_task = asyncio.create_task(waiting_to_nextstate(w, w.event))
        await waiter_task

        if w.MACHINE_STATUS == 'OFF':
            await publish_message(w, client, "app", "get", "STATUS", w.MACHINE_STATUS)
            restart = asyncio.create_task(MachineRestart(w, w.event))
            await restart

        if w.MACHINE_STATUS == 'READY':
            await publish_message(w, client, "app", "get", "STATUS", w.MACHINE_STATUS)

            # door close
            await publish_message(w, client, "app", "get", "STATUS", S_DOORCLOSED)

            # fill water untill full level detected within 10 seconds if not full then timeout
            print(f"{time.ctime()} - [{w.SERIAL}-{w.MACHINE_STATUS}] Filling water...")
            w.MACHINE_STATUS = 'FILLWATER'
            await publish_message(w, client, "app", "get", "STATUS", S_FILLWATER)
            w.task = asyncio.create_task(waiting(w, 'FAULT', 'TIMEOUT'))
            await w.task

        if w.MACHINE_STATUS == 'HEATWATER':
            await publish_message(w, client, "app", "get", "STATUS", w.MACHINE_STATUS)
            # heat water until temperature reach 30 celcius within 10 seconds if not reach 30 celcius then timeout
            print(f"{time.ctime()} - [{w.SERIAL}-{w.MACHINE_STATUS}] Heating water...")
            w.task = asyncio.create_task(waiting(w, 'FAULT', 'TIMEOUT'))
            await w.task

            # wash 10 seconds, if out of balance detected then fault
        if w.MACHINE_STATUS == 'WASH':
            await publish_message(w, client, "app", "get", "STATUS", w.MACHINE_STATUS)
            print(f"{time.ctime()} - [{w.SERIAL}-{w.MACHINE_STATUS}] Still washing...")
            w.task = asyncio.create_task(waiting(w, 'FAULT', 'OUTOFBALANCE'))
            await w.task

            # rinse 10 seconds, if motor failure detect then fault
        if w.MACHINE_STATUS == 'RINSE':
            await publish_message(w, client, "app", "get", "STATUS", w.MACHINE_STATUS)
            print(f"{time.ctime()} - [{w.SERIAL}-{w.MACHINE_STATUS}] Still rinsing...")
            w.task = asyncio.create_task(waiting(w, 'FAULT', 'MOTORFAILURE'))
            await w.task

            # spin 10 seconds, if motor failure detect then fault
        if w.MACHINE_STATUS == 'SPIN':
            await publish_message(w, client, "app", "get", "STATUS", w.MACHINE_STATUS)
            print(f"{time.ctime()} - [{w.SERIAL}-{w.MACHINE_STATUS}] Still spinning...")
            w.task = asyncio.create_task(waiting(w, 'FAULT', 'MOTORFAILURE'))
            await w.task

        if w.MACHINE_STATUS == 'FAULT':
            await publish_message(w, client, "app", "get", "STATUS", w.FAULT_TYPE)
            print(f"{time.ctime()} - [{w.SERIAL}] Waiting to clear fault...")
            await waiter_task
            # ready state set 

            # When washing is in FAULT state, wait until get FAULTCLEARED

        wait_next = round(5*random.random(),2)
        print(f"sleep {wait_next} seconds")
        await asyncio.sleep(wait_next)

async def listen(w, client):
   async with client.messages() as messages:
        await client.subscribe(f"v1cdti/hw/set/{student_id}/model-01/{w.SERIAL}")
        print(f"{time.ctime()} - [{w.SERIAL}] SUB topic: v1cdti/hw/set/{student_id}/model-01/{w.SERIAL}")
        
        await client.subscribe(f"v1cdti/app/get/{student_id}/model-01/")
        print(f"{time.ctime()} - [{w.SERIAL}] SUB topic: v1cdti/app/get/{student_id}/model-01/")

        async for message in messages:
            m_decode = json.loads(message.payload)

            if message.topic.matches(f"v1cdti/app/get/{student_id}/model-01/"):
                await publish_message(w, client, "app", "monitor", "STATUS", w.MACHINE_STATUS)

            if message.topic.matches(f"v1cdti/hw/set/{student_id}/model-01/{w.SERIAL}"):
                # set washing machine status
                print(f"{time.ctime()} - MQTT [{m_decode['serial']}]:{m_decode['name']} => {m_decode['value']}")
                if (m_decode['name']=="STATUS"):
                    w.MACHINE_STATUS = m_decode['value']
                    w.event.set()

                if w.MACHINE_STATUS == 'FILLING':
                    if m_decode['name'] == "WATERLEVEL":
                        if m_decode['value'] == 'FULL':
                            w.MACHINE_STATUS = 'HEATING'
                            print(f'{time.ctime()} - [{w.SERIAL}] STATUS: {w.MACHINE_STATUS}')
                            await publish_message(w, client, 'hw', 'get', 'STATUS', w.MACHINE_STATUS)
                            await w.task.cancel()

                if w.MACHINE_STATUS == 'HEATING':
                    if m_decode['name'] == "TEMPERATURE":
                        if m_decode['value'] == 'REACH':
                            w.MACHINE_STATUS = 'WASH'
                            print(f'{time.ctime()} - [{w.SERIAL}] STATUS: {w.MACHINE_STATUS}')
                            await publish_message(w, client, 'hw', 'get', 'STATUS', w.MACHINE_STATUS)

                if w.MACHINE_STATUS == 'WASH':
                    if m_decode['name'] == "FAULT":
                        w.MACHINE_STATUS = 'FAULT'
                        w.FAULT_TYPE = 'OUTOFBALANCE'
                        await publish_message(w, client, 'hw', 'get', 'STATUS', w.MACHINE_STATUS)
                        await w.task.cancel()
                
                if w.MACHINE_STATUS == 'RINSE':
                    if m_decode['name'] == "FAULT":
                        w.MACHINE_STATUS = 'FAULT'
                        w.FAULT_TYPE = 'MOTORFAILURE'
                        await publish_message(w, client, 'hw', 'get', 'STATUS', w.MACHINE_STATUS)
                        await w.task.cancel()
                
                if w.MACHINE_STATUS == 'SPIN':
                    if m_decode['name'] == "FAULT":
                        w.MACHINE_STATUS = 'FAULT'
                        w.FAULT_TYPE = 'MOTORFAILURE'
                        await publish_message(w, client, 'hw', 'get', 'STATUS', w.MACHINE_STATUS)
                        await w.task.cancel()

                if m_decode['name'] == "FAULT":
                    if m_decode['value'] == 'FAULTCLEAR':
                        w.MACHINE_STATUS = 'OFF'
                        await publish_message(w, client, 'hw', 'get', 'STATUS', w.MACHINE_STATUS)

                        await w.task.cancel()
                w.event.set()


async def main():
    machines = 1
    wl = [WashingMachine(serial=f'SN-00{n}') for n in range(1,machines+1)]
    async with aiomqtt.Client("broker.hivemq.com") as client:
        l = [listen(w, client) for w in wl]
        c = [CoroWashingMachine(w, client) for w in wl]

        await asyncio.gather(*l , *c)


# Change to the "Selector" event loop if platform is Windows
if sys.platform.lower() == "win32" or os.name.lower() == "nt":
    from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())
# Run your async application as usual

asyncio.run(main())