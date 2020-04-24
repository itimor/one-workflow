# -*- coding: utf-8 -*-
# author: itimor

from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {}
        object_list = 'results'
        try:
            meta_dict = getattr(renderer_context.get('view').get_serializer().Meta, 'meta_dict')
        except:
            meta_dict = dict()

        try:
            data.get('paginated_results')
            response_data['meta'] = data['meta']
            response_data[object_list] = data['results']
        except:
            response_data[object_list] = data
            response_data['meta'] = dict()
            response_data['meta'].update(meta_dict)

        response = super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)
        return response
