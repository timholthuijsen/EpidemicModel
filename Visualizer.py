#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import plotly.graph_objects as go
import plotly
import networkx as nx

import numpy as np

#This function output an HTML file which allows to visualize the given SIRS model. 
#INPUT: 
#-G: whose noes have SIRS attributes, i.e., each node has attribute 'state' which consists of a 
#list L of length nb_frames such tha L[t] is 0 if at time t the node is in state S, is 1 if it is in state I, 
# and it is 2 if the node is in state R. 
#-filename: the name of the html file to be generated.
#-beta: the transmission probability.
#gamma: the recovering probability.
#zeta: is the rate in which R individual become S.
#nb_framea: length of the simulation.
#data: a list L of length nb_frames such that L[t] is a list [NS,NI,NR] representing the number of nodes in stat S, state I,
# and state R, at time t.
def showSIRS(G,filename,beta,gamma,xi,nb_frames,data):
    #nodes potitions
    positions=nx.spring_layout(G, iterations=600)# iterations may slow the algorithm quite a bit
    print("Nodes positions computed.")
    
    #start initialising the edge trace
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = positions[edge[0]]
        x1, y1 = positions[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        
    
    edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
                      hoverinfo='none',
                      mode='lines')
    print("Edges trace computed.")

    #construction of the node trace
    node_x,node_y=zip(*list(positions.values()))
    node_trace=[]
    #computation of the list of colour of each node col[n] will be the colour of the nth node in the current frame
    for t in range(nb_frames):
        col=[]
        for n in G:
            if G.nodes[n]['state'][t]==1:
                col.append('red')
            else:
                if G.nodes[n]['state'][t]==0:
                    col.append('blue')
                else:
                    col.append('green')
        #set the attributes the nodes trace sizes, position, colours etc.
        node_trace.append({
                'x':node_x, 'y':node_y,
                'mode':'markers',
                'hoverinfo':'text',
                'marker':{
                        'size':15,
                        'color':col,
                        'line_width':3}})
    print("Nodes trace computed.")
    
    #computing the list of frames to be visulaized
    frames=[{'data':[edge_trace, node_trace[k]],
                 'layout':{
                    #change this if you want to change the information visualized at the top of the page 
                    'title':'<br>S (blue): '+str(data[k][0])+' I (red):'+str(data[k][1])+' R (green): '+str(data[k][2]),
                    'titlefont_size':16},
    'name':str(k)} 
    for k in range(nb_frames)]
    
    
    print("Frames computed.")
    
    #initialization of the sliders that are shown under the simulation 
    sliders = [
                {
                    "pad": {"b": 10, "t": 60},
                    "len": 0.9,
                    "x": 0.1,
                    "y": 0,
                    "steps": [
                        {
                            "args": [[str(k)], {
                "frame": {"duration": 0},
                "mode": "immediate",
                "fromcurrent": True,
                "transition": {"duration": 0, "easing": "linear"},
            }],
                            "label": str(k),
                            "method": "animate",
                        }
                        for k in range(nb_frames)
                    ],
                }
            ]
    
    #this function initializes the arguments for buttons    
    def frame_args(duration):
        return {
                "frame": {"duration": duration},
                "mode": "immediate",
                "fromcurrent": True,
                "transition": {"duration": duration, "easing": "linear"},
            }
        
    #layout of the visualization
    layout={'titlefont_size':16,
               #set this to true if you want to see the legend lising the traces 
              'showlegend':False,
              'hovermode':'closest',
              'annotations':[ dict(
                        #this is the text shown at the bottom of the visualization
                        text="SIRS model with beta="+str(beta)+" gamma="+str(gamma)+" xi="+str(xi),
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
              'xaxis':dict(showgrid=False, zeroline=False, showticklabels=False),
              'yaxis':dict(showgrid=False, zeroline=False, showticklabels=False),
              #'width':700,
              #'height':700,
              'updatemenus' : [
                {
                    "buttons": [
                        {
                            "args": [None, frame_args(500)],
                            "label": "&#9654;", # play symbol
                            "method": "animate",
                        },
                        {
                            "args": [[None], frame_args(500)],
                            "label": "&#9612;&#9612;",#"&#9724;", # pause symbol
                            "method": "animate",
                        },
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 70},
                    "type": "buttons",
                    "x": 0.1,
                    "y": 0,
                }
             ],
            'sliders':sliders
            }

    fig = {'data':[edge_trace, node_trace[0]],
                 'layout':layout,
    'frames':frames}
    
    print("Figure generated.")             
                
    
    print("Visualization rendering done")
    plotly.offline.plot(fig, filename=filename+"_graph.html", auto_open=True, validate=False)
    print("File saved.")



def showData(data,filename,beta,gamma,xi):
    data=np.array(data)
    t=list(range(len(data)))
    #slice the coloumns of the given matrix (note that the input is just a matrix xXn)
    y=data[:,0]
    y1=data[:,1]
    y2=data[:,2]
    
    sliders = [{
                    "pad": {"b": 10, "t": 60},
                    "len": 0.9,
                    "x": 0.1,
                    "y": 0,
                    "steps": [
                        {
                            "args": [[str(k)], {
                "frame": {"duration": 0},
                "mode": "immediate",
                "fromcurrent": True,
                "transition": {"duration": 0, "easing": "linear"},
            }],
                            "label": str(k),
                            "method": "animate",
                        }
                        for k in range(len(t))
                    ],
                }
            ]
    # Create figure
    fig = {
        'data':[
            #trace for S individuals
            {'x':t, 'y':y,
                         'mode':"lines",
                         'name':"Susceptible",
                         'line':dict(width=2, color="blue")},
             #trace for I individuals
              {'x':t, 'y':y1,
                         'mode':"lines",
                         'name':"Infected",
                         'line':dict(width=2, color="red")},
               #trace for R individuals
               {'x':t, 'y':y2,
                         'mode':"lines",
                         'name':"Recovered",
                         'line':dict(width=2, color="green")},
               #traces for the moving dots
               {
                'x':[0],
                'y':[data[0][0]],
                'mode':"markers",
                'marker':dict(color="blue", size=10)}, 
               {
                'x':[0],
                'y':[data[0][1]],
                'mode':"markers",
                'marker':dict(color="red", size=10)},
               {
                'x':[0],
                'y':[data[0][2]],
                'mode':"markers",
                'marker':dict(color="green", size=10)}],
        'layout':{
            'xaxis':dict(range=[0, len(t)], autorange=False, zeroline=False),
            'yaxis':dict(range=[-1, max(y)+10], autorange=False, zeroline=False),
            'title_text':"SIRS model data with beta="+str(beta)+" gamma="+str(gamma)+" xi="+str(xi),
            'hovermode':"closest",
            'updatemenus': [
                {
                    "buttons": [
                        {
                            "args": [None,{"frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                            "label": "&#9654;", # play symbol
                            "method": "animate",
                        },
                        {
                            "args": [[None],{"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                            "label": "&#9612;&#9612;",#"&#9724;", # pause symbol
                            "method": "animate",
                        },
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 70},
                    "type": "buttons",
                    "x": 0.1,
                    "y": 0,
                }
             ],
            'sliders':sliders},
        #initialization of the frame list
        'frames':[{
            'data':[{'x':t, 'y':y,
                         'mode':"lines",
                         'name':"Susceptible",
                         'line':{'width':2, 'color':"blue"}},
                {'x':t, 'y':y1,
                         'mode':"lines",
                         'name':"Infected",
                         'line':{'width':2, 'color':"red"}},
                {'x':t, 'y':y2,
                         'name':"Recovered",
                         'mode':"lines",
                         'line':{'width':2, 'color':"green"}},
                {
                'x':[k],
                'y':[data[k][0]],
                'mode':"markers",
                'name':"Susceptible at t",
                'marker':{'color':"blue", 'size':10}}, 
                {'x':[k],
                'y':[data[k][1]],
                'mode':"markers",
                'name':"Infected at t",
                'marker':{'color':"red", 'size':10}},
                {'x':[k],
                'y':[data[k][2]],
                'mode':"markers",
                'name':"Recovered at t",
                'marker':{'color':"green", 'size':10}}
                ],
            'layout':{
                    'title':"SIRS model data with beta="+str(beta)+" gamma="+str(gamma)+" xi="+str(xi),
                    'titlefont_size':16},
            'name':str(k)}          
            for k in range(len(t))],
    }
    plotly.offline.plot(fig, filename=filename+"_data.html", auto_open=True, validate=False)


