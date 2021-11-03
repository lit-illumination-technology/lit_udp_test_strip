#!/usr/bin/python3
import argparse
import socket
import struct
import tkinter as tk
import time
SCALE = 3
LED_SIZE = 10

def get_args():
    parser = argparse.ArgumentParser(description='LIT test range.')
    parser.add_argument('--port', type=int, default=9000,
                        help='Port number of the virtual range')
    parser.add_argument('--num_leds', type=int, default=60,
                        help='The number of leds in the range.')

    return parser.parse_args()

def start():
    args = get_args()
    
    packet_size = args.num_leds*3 + 8
    root = tk.Tk()
    root.title('LIT test section')
    root.resizable(True, True)
    canvas = tk.Canvas(root, width=args.num_leds*LED_SIZE*SCALE, height=LED_SIZE*SCALE)
    canvas.pack()
    leds=[canvas.create_rectangle(i*SCALE*LED_SIZE, 0, (i+1)*SCALE*LED_SIZE, SCALE*LED_SIZE, fill='black') for i in range(args.num_leds)]
    canvas.update()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", args.port))

    while True:
        data = sock.recv(packet_size)
        if len(data) != packet_size:
            print('ERROR: Incorrect packet size. Expected {} bytes but recieved {}'.format(packet_size, len(data)))
        else:
            for i, led in enumerate(leds):
                rgb = (data[3*i], data[3*i+1], data[3*i+2])
                canvas.itemconfig(led, fill='#{:0>2X}{:0>2X}{:0>2X}'.format(*rgb))
                time = struct.unpack('<q',data[-8:])[0]
                print(time)
            canvas.update()

if __name__ == '__main__':
    start()
