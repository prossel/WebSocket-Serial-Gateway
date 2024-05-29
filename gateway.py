# WebSocket server that forwards messages between a serial port and a WebSocket client
# The serial port is opened when a WebSocket client connects and closed when the client disconnects
# The serial port is read in a separate task to avoid blocking the WebSocket handler

# install modules
# pip3 install websockets pyserial

# Usage: python3 gateway.py [device] [baudrate] [host] [port]
# Usage dev: nodemon --exec python3 gateway.py [device] [baudrate] [host] [port]

# Simple test https://editor.p5js.org/prossel/sketches/fxODyCmxV
# WebSocket Serial Monitor https://editor.p5js.org/prossel/sketches/zTU-rAJM6

# Original repository:
# https://github.com/prossel/WebSocket-Serial-Gateway

# History:
# 2024-05-21 - Pierre Rossel - Initial version
# 2024-05-29 - Pierre Rossel - Added serial port listing, command line parameters and path parameters
#                              Display the list of available serial ports at startup
#                              Use last available port if /last is specified as serial port


import asyncio
import websockets
import serial
from serial.tools import list_ports

# Serial port configuration
ser_port = '/last'
ser_baudrate = 115200

# WebSocket configuration
ws_host = 'localhost'
ws_port = 8765

async def serial_task(ser, websocket):
    print("Serial handler started")
    try:
        while True:
            
            # Get waiting data from serial port
            if ser.in_waiting:
                data = ser.read(ser.in_waiting).decode('utf-8')
                print(f'Received from serial port: {data}')
                await websocket.send(data)

            # let other tasks run
            await asyncio.sleep(0.001)
            
            # print("Serial handler running") 
    except asyncio.CancelledError:
        print("Serial handler cancelled")
        return
    except Exception as e:
        print(f"Serial handler error: {e}")
        return

async def websocket_handler(websocket, path):
    
    print("WebSocket handler started with path: ", path)
    
    if path == "/list":
        # print("Listing serial ports")
        ports = list_ports.comports()
        for port in ports:
            # print(port.device)
            await websocket.send(port.device)
        return
    
    # path may contain optional serial port and baudrate 
    # Examples: 
    # - /
    # - /@
    # - /dev/tty.usbmodem101
    # - /dev/tty.usbmodem101@
    # - /dev/tty.usbmodem101@115200
    
    # extract serial port and baudrate from path
    global ser_port
    global ser_baudrate
    if path != "/":
        parts = path.split('@')
        if len(parts[0]) > 1: 
            ser_port = parts[0]
        if len(parts) > 1 and len(parts[1]) > 0:
            ser_baudrate = int(parts[1])
    
    # special case: port /last will use last available port
    if ser_port == "/last":
        ports = list_ports.comports()
        ser_port = ports[-1].device
    
    print("Waiting for port " + ser_port + " at " + str(ser_baudrate) + " bauds")
    
    while websocket.open:

        # Open the serial port
        try:
            ser = serial.Serial(ser_port, ser_baudrate)
            print(f'Serial port open on {ser_port} at {ser_baudrate} bauds')
        except serial.SerialException as e:
            # print(f"Serial port open error: {e}")
            # wait 2 seconds before retrying
            await asyncio.sleep(2)
            continue

        # Start the serial handler
        taskSerial = asyncio.create_task(serial_task(ser, websocket))
                
        # Wait for WebSocket messages
        while True:
            # print('.', end='', flush=True)
            
            # get any message from WebSocket
            try:
                print("Waiting for message from WebSocket...")
                message = await websocket.recv()

                print(f'... received from WebSocket: {message}')
                ser.write(message.encode('utf-8'))
            
            # seriaException
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                break
            except websockets.exceptions.ConnectionClosedOK:
                break
            except websockets.exceptions.ConnectionClosedError:
                break
            
        # Stop the serial handler
        print("Candelling serial task")
        taskSerial.cancel()

        # Close the serial port
        print("Closing serial port")
        ser.close()
     
    print("WebSocket handler ended")
    
# get parameters from command line (if any)
# example: python3 gateway.py /dev/tty.usbmodem101 115200 localhost 8765
import sys
if len(sys.argv) > 1:
    ser_port = sys.argv[1]
if len(sys.argv) > 2:
    ser_baudrate = int(sys.argv[2])
if len(sys.argv) > 3:
    ws_host = sys.argv[3]
if len(sys.argv) > 4:
    ws_port = int(sys.argv[4])

print("WebSocket Serial Gateway started")
print("Parameters:")
print(f"  Serial port: {ser_port} at {ser_baudrate} bauds")
print(f"  WebSocket server: {ws_host}:{ws_port}")

print("Serial ports available:")
ports = list_ports.comports()
for port in ports:
    print("  " + port.device)

print("Waiting for WebSocket connections...")
    
try:
    # Start the WebSocket server
    start_server = websockets.serve(websocket_handler, ws_host, ws_port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    print(" Received exit signal in loop, stopping...")
