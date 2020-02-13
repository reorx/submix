from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

from submix.parser import ProxyURLList


class CliState:
    sub_source: str
    sub_content: bytes
    purls: ProxyURLList


cli_state = CliState()


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class NodesView(View):
    def get(self, request):
        return render(request, 'nodes.html', dict(
            cli_state=cli_state,
        ))
