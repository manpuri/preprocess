from typing import List, Dict
import argparse
import json
import logging
import numpy as np
import requests
import cv2
import pandas as pd
import base64

def preprocess(inputs: Dict) -> Dict:
    #return {'instances': [image_transform(instance) for instance in inputs['instances']]}        
    logging.info("inputs %s", str(inputs))
    del inputs['instances']
    try:
        json_data = inputs
    except ValueError:
        return json.dumps({ "error": "Recieved invalid json" })
    data = json_data["signatures"]["inputs"][0][0]["data"].encode()
    csv = json_data["file"]
    with open("/image.png", "wb") as fh:
        fh.write(base64.decodebytes(data))
    f = open("/file.txt", "w")
    f.write(csv)
    f.close()
    test_df = pd.read_csv("/file.txt")
    csv = test_df.drop(['days_to_death','bcr_patient_barcode'], axis = 1)
    csv = np.asarray(csv)
    csv = csv.reshape(csv.shape[0],csv.shape[1],1)
    img = cv2.imread("/image.png", cv2.IMREAD_GRAYSCALE)
    img = img.reshape(1,img.shape[0],img.shape[1],1)
    payload = {
        "inputs": {'csv_input:0': csv.tolist(),'img_input:0': img.tolist()}
    }
    return payload

def postprocess(inputs: List) -> List:
    return inputs
