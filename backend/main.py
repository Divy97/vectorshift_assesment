# /backend/main.py

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
import networkx as nx

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Node(BaseModel):
    id: str
    data: dict

class Edge(BaseModel):
    source: str
    target: str

class PipelineData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

def calculate_pipeline_stats(nodes, edges):
    num_nodes = len(nodes)
    num_edges = len(edges)

    graph = nx.DiGraph()
    graph.add_nodes_from(node.id for node in nodes)
    graph.add_edges_from((edge.source, edge.target) for edge in edges)

    is_dag = nx.is_directed_acyclic_graph(graph)

    print (num_nodes)
    return {'num_nodes': num_nodes, 'num_edges': num_edges, 'is_dag': is_dag}

@app.post('/pipelines/parse')
async def parse_pipeline(pipeline_data: PipelineData):
    nodes = pipeline_data.nodes
    edges = pipeline_data.edges

    try:
        pipeline_stats = calculate_pipeline_stats(nodes, edges)
        return pipeline_stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
