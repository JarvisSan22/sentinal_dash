# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 10:05:44 2021

@author: dev
"""
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import date
import aurth
import numpy as np
import Sentinal_image as SI
from PIL import Image
import base64
from io import BytesIO



def pil_to_b64(im, enc="png"):
    io_buf = BytesIO()
    im.save(io_buf, format=enc)
    encoded = base64.b64encode(io_buf.getvalue()).decode("utf-8")
    return f"data:img/{enc};base64, " + encoded
# Dash component wrappers
def Row(children=None, **kwargs):
    return html.Div(children, className="row", **kwargs)


app = dash.Dash(__name__)
Title="Sentinal dash"
Values=["TRUE_IMG","CO","NO"]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app.layout = html.Div([
      #Otopn buttons 
      Row(html.H1(Title)),
      html.Div([
   #   ddc.DataPickerRange(
    #      id="date_picker",
     #     min_date_allowed=data(2018,1,1),
      #    max_date_allowed=data.today(),
      #    initial_visible_month=
          
       #   )
       
      dcc.DatePickerSingle(
        id='date_picker',
        min_date_allowed=date(2018, 1, 1),
        max_date_allowed=date.today(),
        initial_visible_month=date(2018, 1, 1),
        date=date(2018, 1, 1)
      ), 
   #   dcc.Input(id="box_input", type="text", placeholder="[140.5755615,35.1693180,139.0759277,35.7821707]"),
      dcc.Dropdown(
          id="img_val",
          options=[{"label": x, "value": x} 
                   for x in Values],
          value=Values[0], 
      ),
    
      dcc.Graph(id="sat_image"),
      
  ])])
                   
                   

@app.callback(
    Output("sat_image", "figure"), 
    [Input("date_picker", "date"), #Input("box_input", "value"),
     Input("img_val","value")])

def addimage(date_picker,img_val):
        
    imagestypes=["TRUE_IMG","CO","NO"]
    day=str(date_picker)
    print(day)
    #bbox=box_input[1:~0].split(",")
    bbox=[
    139.0759277,
    35.1693180,
    140.5755615, 
    35.7821707,
    ]
    #左回りもしくは右回り時の対応
    for i in range(len(bbox)):
       # bbox[i]=float(bbox[i])
        
        if bbox[i] >= 0:
            bbox[i] = bbox[i]%360
        else:
            bbox[i] = -(abs(bbox[i])%360) + 360
            
    # Create figure
    fig = go.Figure()
    TOKEN=aurth.getToken()
    
   
    if img_val=="TRUE_IMG":
        #img=SI.get_img(bbox,day,img_val,TOKEN )
        img=SI.get_s2_true_img(bbox,day,TOKEN )
    elif img_val=="CO":
         img=SI.get_co_img(bbox, day,TOKEN)
    elif img_val=="NO":
        img=SI.get_NO_img(bbox, day,TOKEN)
    img_width =  512
    img_height =512
    scale_factor = 0.5
    img= Image.fromarray(np.uint8(img))
    
    fig.add_layout_image(dict(
    source=pil_to_b64(img), sizing="stretch", opacity=1, layer="below",
    x=0, y=0, xref="x", yref="y", sizex=img_width, sizey=img_height,))
    
    
    fig.update_xaxes(
        showgrid=False, visible=False, constrain="domain", range=[0, img_width])
    
    
    fig.update_xaxes(
        showgrid=False, visible=False, constrain="domain", range=[0, img_width])
    
    fig.update_yaxes(
        showgrid=False, visible=False,
        scaleanchor="x", scaleratio=1,
        range=[img_height, 0])
    
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)