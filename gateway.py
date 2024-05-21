# Websocket server that forwards messages between a serial port and a websocket client
# The serial port is opened when a websocket client connects and closed when the client disconnects
# The serial port is read in a separate task to avoid blocking the websocket handler

# Usage: python3 gateway.py
# Usage dev: nodemon --exec python3 gateway.py

# 2024-05-21 - Pierre Rossel - Initial version


import asyncio
import websockets
import serial

# Paramètres du port série
ser_port = '/dev/tty.usbmodem2101'
ser_baudrate = 9600

# Paramètres du websocket
ws_host = 'localhost'
ws_port = 8765

async def serial_task(ser, websocket):
    print("Serial handler started")
    while True:
        
        # Get waiting data from serial port
        if ser.in_waiting:
            data = ser.read(ser.in_waiting).decode('utf-8')
            print(f'Received from serial port: {data}')
            await websocket.send(data)

        # let other tasks run
        await asyncio.sleep(0.001)
        
        # print("Serial handler running") 
        

async def websocket_handler(websocket, path):
    
    # Ouvrir le port série
    ser = serial.Serial(ser_port, ser_baudrate)
    print(f'Port série ouvert sur {ser_port} à {ser_baudrate} bauds')

    # Start the serial handler
    taskSerial = asyncio.create_task(serial_task(ser, websocket))

    while True:
        # print('.', end='', flush=True)
        
        # get any message from websocket
        try:
            message = await websocket.recv()

            print(f'Received from websocket: {message}')
            ser.write(message.encode('utf-8'))
            
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
     

start_server = websockets.serve(websocket_handler, ws_host, ws_port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
