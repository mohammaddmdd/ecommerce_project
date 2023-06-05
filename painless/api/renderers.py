from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework import status

class DataStatusMessage_Renderer(JSONOpenAPIRenderer):
        
        def render(self, data, accepted_media_type=None, renderer_context=None):
            
            status_code = renderer_context['response'].status_code
            response = dict()

            # import pdb ; pdb.set_trace()
            if status.is_success(status_code):
                response['detail'] = None

                results_sign = data.get('results', {})
                if type(results_sign) == ReturnList:
                    response['total'] = data['count']
                    response['next'] = data['next']
                    response['previous'] = data['previous']
                    response['results'] = data['results']
                else:
                    response['results'] = data

            elif status.is_client_error(status_code):
                response = data

            elif status.is_server_error(status_code) :
                response['detail'] = "Server Error"
                response['data'] = None

            else:
                response['detail'] = "Message not handled correctly."
                response['data'] = data

            return super().render(response, accepted_media_type, renderer_context)