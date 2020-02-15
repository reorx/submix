from django.views import View
from django.shortcuts import render

from submix.parser import NodeList, Node
from submix.utils import json_response, api_data, make_json_encoder_for_type


class CliState:
    sub_source: str
    sub_content: bytes
    nodes: NodeList


cli_state = CliState()


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class NodesView(View):
    def get(self, request):
        return render(request, 'nodes.html')


node_keys = ['name', 'protocol', 'config']


def format_node(node: Node):
    return {k: getattr(node, k) for k in node_keys}


class APINodesView(View):
    def get(self, request):
        d = api_data(cli_state.nodes)
        return json_response(d, encoder=make_json_encoder_for_type(Node, format_node))
