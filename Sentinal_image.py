# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 07:43:51 2021

@author: dev
"""

import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from io import BytesIO
import cv2
import requests
from PIL import Image
import aurth 
#TOKEN=aurth.TOKEN 

imagetypes_eval={}

imagetypes_eval["TRUE_IMG"]="""
    //VERSION=3
    function setup() {
      return {
        input: ["B02", "B03", "B04"],
        output: { 
          bands: 3, 
          sampleType: "AUTO" // default value - scales the output values from [0,1] to [0,255].
        }
      }
    }
    function evaluatePixel(sample) {
      return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02]
    }
    """


imagetypes_eval["CO"]="""
      //VERSION=3

      function setup() {
        return {
          input: ["CO", "dataMask"],
          output: { bands:  4 }
        }
      }
      const minVal = 0.0
      const maxVal = 0.1
      const diff = maxVal - minVal
      const rainbowColors = [
          [minVal, [0, 0, 0.5]],
          [minVal + 0.125 * diff, [0, 0, 1]],
          [minVal + 0.375 * diff, [0, 1, 1]],
          [minVal + 0.625 * diff, [1, 1, 0]],
          [minVal + 0.875 * diff, [1, 0, 0]],
          [maxVal, [0.5, 0, 0]]
      ]
      const viz = new ColorRampVisualizer(rainbowColors)
      function evaluatePixel(sample) {
          var rgba= viz.process(sample.CO)
          rgba.push(sample.dataMask)
          return rgba
      }
      """


imagetypes_eval["SO"]= """
    //VERSION=3
    function setup() {
      return {
        input: ["B02", "B03", "B04"],
        output: { 
          bands: 3, 
          sampleType: "AUTO" // default value - scales the output values from [0,1] to [0,255].
        }
      }
    }
    function evaluatePixel(sample) {
      return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02]
    }

    """

imagetypes_eval["NO"]:"""
        //VERSION=3

        function setup() {
          return {
            input: ["NO2", "dataMask"],
            output: { bands:  4 }
          }
        }
        const minVal = 0.0
        const maxVal = 0.0001
        const diff = maxVal - minVal
        const rainbowColors = [
            [minVal, [0, 0, 0.5]],
            [minVal + 0.125 * diff, [0, 0, 1]],
            [minVal + 0.375 * diff, [0, 1, 1]],
            [minVal + 0.625 * diff, [1, 1, 0]],
            [minVal + 0.875 * diff, [1, 0, 0]],
            [maxVal, [0.5, 0, 0]]
        ]
        const viz = new ColorRampVisualizer(rainbowColors)
        function evaluatePixel(sample) {
            var rgba= viz.process(sample.NO2)
            rgba.push(sample.dataMask)
            return rgba
        }
        """
    

def get_s2_true_img(bbox,day,TOKEN):
    response = requests.post('https://services.sentinel-hub.com/api/v1/process',
    headers={"Authorization" : f"Bearer {TOKEN}"},
    json={
    "input": {
        "bounds": {
            "properties": {
                "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
            },
            "bbox": bbox
        },
        "data": [
            {
                "type": "S2L2A",
                "dataFilter": {
                    "timeRange": {
                         "from": f"{day}T00:00:00Z",
                          "to": f"{day}T23:59:59Z"
                    }
                }
            }
        ]
    },
    "output": {
        "width": 512,
        "height": 512
    },
    "evalscript": """
    //VERSION=3
    function setup() {
      return {
        input: ["B02", "B03", "B04"],
        output: { 
          bands: 3, 
          sampleType: "AUTO" // default value - scales the output values from [0,1] to [0,255].
        }
      }
    }
    function evaluatePixel(sample) {
      return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02]
    }

    """
    })
    img = Image.fromarray(io.imread(BytesIO(response.content)))
    img.putalpha(alpha=255)
    return np.array(img)
def get_NO_img(bbox, day,TOKEN):
    response = requests.post('https://creodias.sentinel-hub.com/api/v1/process',
    headers={"Authorization" : f"Bearer {TOKEN}"},
    json={
      "input": {
          "bounds": {
                  "properties": {
                  "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
              },
              "bbox": bbox
          },
          "data": [
              {
                  "type": "S5PL2",
                  "dataFilter": {
                      "timeRange": {
                          "from": f"{day}T00:00:00Z",
                          "to": f"{day}T23:59:59Z"
                      },
                      "timeliness": "NRTI"
                  }
              }
          ]
      },
      "output": {
          "width": 512,
          "height": 512
      },
      "evalscript": """
       //VERSION=3

        function setup() {
          return {
            input: ["NO2", "dataMask"],
            output: { bands:  4 }
          }
        }
        const minVal = 0.0
        const maxVal = 0.0001
        const diff = maxVal - minVal
        const rainbowColors = [
            [minVal, [0, 0, 0.5]],
            [minVal + 0.125 * diff, [0, 0, 1]],
            [minVal + 0.375 * diff, [0, 1, 1]],
            [minVal + 0.625 * diff, [1, 1, 0]],
            [minVal + 0.875 * diff, [1, 0, 0]],
            [maxVal, [0.5, 0, 0]]
        ]
        const viz = new ColorRampVisualizer(rainbowColors)
        function evaluatePixel(sample) {
            var rgba= viz.process(sample.NO2)
            rgba.push(sample.dataMask)
            return rgba
        }
      """
    })
    return io.imread(BytesIO(response.content))

def get_so_img(bbox, day,TOKEN):
    response = requests.post('https://creodias.sentinel-hub.com/api/v1/process',
    headers={"Authorization" : f"Bearer {TOKEN}"},
    json={
      "input": {
          "bounds": {
                  "properties": {
                  "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
              },
              "bbox": bbox
          },
          "data": [
              {
                  "type": "S5PL2",
                  "dataFilter": {
                      "timeRange": {
                          "from": f"{day}T00:00:00Z",
                          "to": f"{day}T23:59:59Z"
                      }
                  }
              }
          ]
      },
      "output": {
          "width": 512,
          "height": 512
      },
      "evalscript": """
       //VERSION=3
        function setup() {
          return {
            input: ["B02", "B03", "B04"],
            output: { 
              bands: 3, 
              sampleType: "AUTO" // default value - scales the output values from [0,1] to [0,255].
            }
          }
        }
        function evaluatePixel(sample) {
          return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02]
        }

      """
    })
    return io.imread(BytesIO(response.content))

def get_co_img(bbox, day,TOKEN):
    response = requests.post('https://creodias.sentinel-hub.com/api/v1/process',
    headers={"Authorization" : f"Bearer {TOKEN}"},
    json={
      "input": {
          "bounds": {
                  "properties": {
                  "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
              },
              "bbox": bbox
          },
          "data": [
              {
                  "type": "S5PL2",
                  "dataFilter": {
                      "timeRange": {
                          "from": f"{day}T00:00:00Z",
                          "to": f"{day}T23:59:59Z"
                      }
                  }
              }
          ]
      },
      "output": {
          "width": 512,
          "height": 512
      },
      "evalscript": """
      //VERSION=3

      function setup() {
        return {
          input: ["CO", "dataMask"],
          output: { bands:  4 }
        }
      }
      const minVal = 0.0
      const maxVal = 0.1
      const diff = maxVal - minVal
      const rainbowColors = [
          [minVal, [0, 0, 0.5]],
          [minVal + 0.125 * diff, [0, 0, 1]],
          [minVal + 0.375 * diff, [0, 1, 1]],
          [minVal + 0.625 * diff, [1, 1, 0]],
          [minVal + 0.875 * diff, [1, 0, 0]],
          [maxVal, [0.5, 0, 0]]
      ]
      const viz = new ColorRampVisualizer(rainbowColors)
      function evaluatePixel(sample) {
          var rgba= viz.process(sample.CO)
          rgba.push(sample.dataMask)
          return rgba
      }
      """
    })
    return io.imread(BytesIO(response.content))



def get_img(bbox,day,image_type,TOKEN ):
    

    if image_type in ["SO","TRUE_IMG"] :
        dtype="S2L2A"
    elif image_type in ["CO","NO"]:
        dtype="S5PL2"
        
   
    json={
    "input": {
        "bounds": {
            "properties": {
                "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
            },
            "bbox": bbox
        },
        "data": [
            {
                "type": dtype,
                "dataFilter": {
                    "timeRange": {
                         "from": f"{day}T00:00:00Z",
                          "to": f"{day}T23:59:59Z"
                    }
                }
            }
        ]
    },
    "output": {
        "width": 512,
        "height": 512
    },
    "evalscript": imagetypes_eval[image_type]
    }
    
    if image_type=="NO":
        json["input"]["data"][0]["dataFilter"]["timeliness"]= "NRTI"
    print(json) 
    
    response = requests.post('https://services.sentinel-hub.com/api/v1/process',
    headers={"Authorization" : f"Bearer {TOKEN}"},json=json,)
    
    return  io.imread(BytesIO(response.content))
   

def draw_texts(img, texts, font_scale=0.7, thickness=2):
    h, w, c = img.shape
    offset_x = 10  # 左下の座標
    initial_y = 450
    dy = int(img.shape[1] / 15)
    color = (255, 255, 255, 0)  # black

    texts = [texts] if type(texts) == str else texts

    for i, text in enumerate(texts):
        offset_y = initial_y + (i+1)*dy
        cv2.putText(img, text, (offset_x, offset_y), cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale, color, thickness, cv2.LINE_AA)

def draw_result_on_img(img, texts, w_ratio=0.8, h_ratio=0.2, alpha=0.4):
    # 文字をのせるためのマットを作成する
    overlay = img.copy()
    pt1 = (0, 500)
    pt2 = (int(img.shape[1] * w_ratio), int(img.shape[0] * h_ratio))

    mat_color = (25, 25, 25)
    fill = -1  # -1にすると塗りつぶし
    cv2.rectangle(overlay, pt1, pt2, mat_color, fill)

    mat_img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

    draw_texts(mat_img, texts)

    return mat_img

def add_copyright(img):
    new_img = draw_result_on_img(img, texts=["produced from ESA remote sensing data"], w_ratio=1.0, h_ratio=0.9, alpha=0.5)

    return new_img
def get_concat_h(im1, im2):
        return cv2.hconcat([im1, im2])