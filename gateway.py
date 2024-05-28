# WebSocket server that forwards messages between a serial port and a WebSocket client
# The serial port is opened when a WebSocket client connects and closed when the client disconnects
# The serial port is read in a separate task to avoid blocking the WebSocket handler

# install modules
# pip3 install websockets pyserial

# Usage: python3 gateway.py
# Usage dev: nodemon --exec python3 gateway.py

# Test with https://editor.p5js.org/prossel/sketches/fxODyCmxV

# Original repository:
# https://github.com/prossel/WebSocket-Serial-Gateway

# History:
# 2024-05-21 - Pierre Rossel - Initial version


import asyncio
import websockets
import serial

# Serial port configuration
ser_port = '/dev/tty.usbmodem101'
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
    
    while websocket.open:

        # Open the serial port
        try:
            ser = serial.Serial(ser_port, ser_baudrate)
            print(f'Serial port open on {ser_port} at {ser_baudrate} bauds')
        except serial.SerialException as e:
            print(f"Serial port open error: {e}")
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
    
# Start the WebSocket server
start_server = websockets.serve(websocket_handler, ws_host, ws_port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
