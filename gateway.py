import asyncio
import websockets
import serial

# Paramètres du port série
ser_port = '/dev/tty.usbmodem2101'
ser_baudrate = 9600

# Paramètres du websocket
ws_host = 'localhost'
ws_port = 8765

async def serial_handler():
    print("Serial handler started")
    while True:
        await asyncio.sleep(1)
        print("Serial handler running") 
            
    print("Serial handler stopped")


async def websocket_handler(websocket, path):
    # Ouvrir le port série
    ser = serial.Serial(ser_port, ser_baudrate)
    print(f'Port série ouvert sur {ser_port} à {ser_baudrate} bauds')

    # Start the serial handler
    mySerial = asyncio.create_task(serial_handler())
    
    # Attendre les données du port série et les envoyer au websocket
    

    while True:
        print('.', end='', flush=True)
        
        
        # Get waiting data from serial port
        if ser.in_waiting:
            # line = ser.readline().decode('utf-8').strip()
            # print(f'Received from serial port: {line}')
            # await websocket.send(line)
            
            data = ser.read(ser.in_waiting).decode('utf-8')
            print(f'Received from serial port: {data}')
            await websocket.send(data)
        
        # if there is any message from websocket, send it to serial port. Don't wait for it.
        # This is to avoid blocking the serial port reading
        
        # if (websocket.messages):
            # message = await websocket.recv()
            # print(f'Received from websocket: {message}')
            # ser.write(message.encode('utf-8'))
        
        # get any message from websocket
        try:
            message = await websocket.recv()

            print(f'Received from websocket: {message}')
            ser.write(message.encode('utf-8'))
            
        except websockets.exceptions.ConnectionClosedOK:
            break
        except websockets.exceptions.ConnectionClosedError:
            break
        
        
    # Fermer le port série
    ser.close()
    print('Port série fermé')    
       
    # Stop the serial handler
    mySerial.cancel()
    print("Serial handler stopped")
     

start_server = websockets.serve(websocket_handler, ws_host, ws_port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
