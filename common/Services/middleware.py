import logging

logger = logging.getLogger('page_access')

class PageAccessLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.path != '/favicon.ico':
            user_info = request.user.username if request.user.is_authenticated else 'Anonymous'
            logger.info(f'{user_info}\t -> \t{request.path}')
        
        return response
