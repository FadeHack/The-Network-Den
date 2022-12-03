from threading import local
from flask import Flask,request
import pyshark
import time
import nest_asyncio
nest_asyncio.apply()
import pandas as pd
import openpyxl
from flask_ngrok import run_with_ngrok
wb = openpyxl.Workbook()  
sheet = wb.active
def cellEntry(row, column, attribute):
    new_cell = sheet.cell(row, column)
    new_cell.value = str(attribute)


cellEntry(1,1,"Localtime")
cellEntry(1,2,"Source IP")
cellEntry(1,3,"Source Port")
cellEntry(1,4,"Destination IP")
cellEntry(1,5,"Destination Port")
cellEntry(1,6,"Protocol")
app = Flask(__name__)


@app.route("/saveascsv",methods = ["POST"])
async def saveascsv():
    row1 = 2
    global capture
    networkI = request.get_json()
    networkInterface = str(networkI["networkInterface"])
    print(networkInterface)
    
    capture = pyshark.LiveCapture(interface = networkInterface)
    
    print(capture)
    for packet in capture.sniff_continuously():
        try:
            localtime = time.asctime(time.localtime(time.time()))
            cellEntry(row1,1,localtime)
            protocol = packet.transport_layer
            cellEntry(row1,6,protocol)
            src_addr = packet.ip.src 
            cellEntry(row1,2,src_addr)
            src_port = packet[protocol].srcport
            cellEntry(row1,3,src_port)
            dst_addr = packet.ip.dst
            cellEntry(row1,4,dst_addr)
            dst_port = packet[protocol].dstport 
            cellEntry(row1,5,dst_port)
            wb.save("log.xlsx")
            row1=row1+1

            # print ("%s IP %s:%s <-> %s:%s (%s)" % (localtime, src_addr, src_port, dst_addr, dst_port, protocol))
            # time.sleep(3)
        except AttributeError as e:
            pass
            print (" ")
    
        

if __name__ == "__main__":
    app.run(debug=True)
    