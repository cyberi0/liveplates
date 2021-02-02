from openalpr import Alpr
import cv2
from tkinter import *
from datetime import datetime
from flask import Flask, jsonify, request
import MySQLdb

conn = None
lastPlate = ""
reportPlate = None
app = Flask(__name__)


def connect_mysql():
    global conn
    try:
        conn = MySQLdb.connect(host="localhost", user="root", passwd="m0rph1n3", db="tagger")
    except MySQLdb.Error:
        print("Error de Conexión MySQL")
    if conn.open:
        print("Conexión Satisfactoria MySQL")


def access_tagger(plate_access):
    if len(plate_access) >= 7:
        cursor = conn.cursor()
        access_date = datetime.now()
        try:
            query = 'INSERT INTO plates(plate, access_date) VALUES( "' + plate_access + '", CURRENT_TIMESTAMP )'
            cursor.execute(query)
            conn.commit()
        except:
            conn.rollback()
        cursor.close()


def black_list_insert(data, plate_access):
    cursor = conn.cursor()
    access_date = datetime.now()
    try:
        query = 'INSERT INTO black_list(plate, description, report_date) ' \
                + ' VALUES( "' + plate_access + '", "' + data['description'] + '", CURRENT_TIMESTAMP ) '
        cursor.execute(query)
        conn.commit()
        response_json = {
            'status': 200,
            'message': "Placa: " + plate_access + " Reportada",
            'payload': {
                'plate': plate_access,
                'description': data['description']
            }
        }
        return jsonify(response_json)
    except:
        response_json = {
            'status': 500,
            'message': "Ocurrió un error durante la ejecución"
        }
        return jsonify(response_json)
        conn.rollback()
    cursor.close()


def black_list(plate_access):
    if len(plate_access) >= 7:
        cursor = conn.cursor()
        access_date = datetime.now()
        try:
            query = 'SELECT * FROM black_list WHERE plate = "' + plate_access + '"'
            cursor.execute(query)
            in_black_list = cursor.fetchone()

            if in_black_list is None:
                response_json = {
                    'status': 200,
                    'message': "Placa: " + plate_access + " Con Acceso Permitido",
                    'payload': {
                        'plate': plate_access,
                        'description': 'Lorem Ipsum Dolor'
                    }
                }
            else:
                response_json = {
                    'status': 300,
                    'message': "Acceso Restringido para " + plate_access,
                    'payload': {
                        'plate': plate_access,
                        'description': 'Lorem Ipsum Dolor',
                    }
                }
        except:
            response_json = {
                'status': 500,
                'message': "Ocurrió un error durante la ejecución"
            }
        cursor.close()

        return jsonify(response_json)


def start_capture_plates(rtsp):
    cap = cv2.VideoCapture(rtsp)
    global lastPlate

    alpr = Alpr("mx", "openalpr.conf", "runtime_data")
    if not alpr.is_loaded():
        print("Error al Cargar Librería: OpenALPR")

    alpr.set_top_n(20)
    alpr.set_default_region("mx")

    if alpr.is_loaded():
        while cap.isOpened():
            ret, img = cap.read()
            img_str = cv2.imencode('.jpg', img)[1].tostring()
            # cv2.imshow('img', img)

            results = alpr.recognize_array(img_str)
            print(results)

            for plate in results['results']:
                len_plate = len(plate['plate'])
                if len_plate == 7:
                    cv2.putText(img, plate['plate'],
                                (plate['coordinates'][0]['x'], plate['coordinates'][0]['y'])
                                , 0, 2, (255, 0, 0), 3)
                    cv2.rectangle(img, (plate['coordinates'][0]['x'], plate['coordinates'][0]['y']),
                                  (plate['coordinates'][2]['x'], plate['coordinates'][2]['y']), (255, 0, 0), 3)
                    cv2.imshow('img', img)
                    report_plate = black_list(plate['plate'])
                    if report_plate.status == 200:
                        access_tagger(plate['plate'])
                        lastPlate = plate['plate']
                        response_json = {
                            'message': 'Acceso Permitido',
                            'payload': {
                                'plate': lastPlate,
                                'description': 'Lorem Ipsum Dolor'
                            }
                        }
                        alpr.unload()
                        cv2.destroyAllWindows()
                        return jsonify(response_json)
                    else:
                        alpr.unload()
                        cv2.destroyAllWindows()
                        response_json = report_plate
                        return response_json


'''
 ___________________________________________________________________________
| Search Plates                                                             |
|___________________________________________________________________________|
| Endpoint: /plates/search
|
| Get Plate Report. You can Get a short description about Plate if you
| send a valid JSON with the next structure:
|   {
|       "rtsp" : 0    // Zero For Localhost. 
|                        Or you can type a valid rtsp camera IP: 
|                        ["rtsp://admin:123456@192.168.0.333"]
|   }
|
|___________________________________________________________________________
| Response                                                                  |
|___________________________________________________________________________|
|   JSON Response. In case plate founded in Blacklist:
|
|   {
|    "message": "Acceso Restringido para YJB1312",
|    "payload": {
|        "description": "Lorem Ipsum Dolor",
|        "plate": "YJB1312"
|    },
|    "status": 300
|   }
|
|___________________________________________________________________________
|
|   JSON Response. In case plate not founded in Blacklist:
|
|   {
|        "message": "Placa: YJB1312 Con Acceso Permitido",
|        "payload": {
|            "description": "Lorem Ipsum Dolor",
|            "plate": "YJB1312"
|       },
|        "status": 200
|    }
|
|___________________________________________________________________________
'''


@app.route("/plates/search", methods=['POST'])
def plates_info():
    data = request.get_json()
    connect_mysql()
    response_json = start_capture_plates(data['rtsp'])
    return response_json


def start_capture_plates_blacklist(data):
    cap = cv2.VideoCapture(data['rtsp'])
    global lastPlate

    alpr = Alpr("mx", "openalpr.conf", "runtime_data")
    if not alpr.is_loaded():
        print("Error al Cargar Librería: OpenALPR")

    alpr.set_top_n(20)
    alpr.set_default_region("mx")

    if alpr.is_loaded():
        while cap.isOpened():
            ret, img = cap.read()
            img_str = cv2.imencode('.jpg', img)[1].tostring()
            # cv2.imshow('img', img)

            results = alpr.recognize_array(img_str)
            # print(results)

            for plate in results['results']:
                len_plate = len(plate['plate'])
                if len_plate == 7:
                    cv2.putText(img, plate['plate'],
                                (plate['coordinates'][0]['x'], plate['coordinates'][0]['y'])
                                , 0, 2, (255, 0, 0), 3)
                    cv2.rectangle(img, (plate['coordinates'][0]['x'], plate['coordinates'][0]['y']),
                                  (plate['coordinates'][2]['x'], plate['coordinates'][2]['y']), (255, 0, 0), 3)
                    # cv2.imshow('img', img)
                    response_json = black_list_insert(data, plate['plate'])
                    print(response_json)
                    lastPlate = plate['plate']
                    alpr.unload()
                    cv2.destroyAllWindows()
                    return response_json


'''
 ___________________________________________________________________________
| Blacklist Plates                                                          |
|___________________________________________________________________________|
| Endpoint: /plates/blacklist
|
| Insert Plate Report. You can Insert a short description about the report
| Just send a valid JSON with the next structure:
|   {
|       "rtsp" : 0,    // Zero For Localhost. 
|                         Or you can type a valid rtsp camera IP: 
|                         ["rtsp://admin:123456@192.168.0.333"]
|       "description" : "Reporte de Robo en Casa Habitación con Esta placa"
|   }
|
|___________________________________________________________________________
| Response                                                                  |
|___________________________________________________________________________|
|   JSON Response. Inserted in DB:
|   {
|        "message": "Placa: YHZ1926 Reportada",
|        "payload": {
|            "description": "Reporte de Robo en Casa Habitación con Esta placa",
|            "plate": "YHZ1926"
|        },
|        "status": 200
|    }
|
|___________________________________________________________________________

'''


@app.route("/plates/blacklist", methods=['POST'])
def plates_blacklist():
    data = request.get_json()
    connect_mysql()
    response_json = start_capture_plates_blacklist(data)
    print(response_json)
    return response_json


if __name__ == "__main__":
    app.run()
