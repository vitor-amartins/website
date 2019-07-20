from django.shortcuts import render
from core.models import Link
from core.utils import get_color
from rest_framework import generics
from core.serializers import LinkSerializer


def tree(request):
    links = Link.objects.all().values('link', 'descricao', 'cor')
    for link in links:
        link['cor_extenso'] = get_color(link['cor'])
    return render(request, "tree.html", {"links": links})


class LinkList(generics.ListAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
