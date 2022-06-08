import os
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param


def delete_file(path):
   """ Deletes file from filesystem 
   """
   if os.path.isfile(path):
       os.remove(path)



DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10

class CustomPaginator(PageNumberPagination):
    """
    Custom pagination for api response
    """
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_next_link(self,album_id=None):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri().split('api')[0]
        page_number = self.page.next_page_number()
        new_link = f"{url}api/v1/album/get-albums-track/{album_id}?page={page_number}"
        return new_link

    def get_paginated_response(self, data, album_id=None):
        return Response({
            'links': {
                'next': self.get_next_link(album_id),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'items': data
        })