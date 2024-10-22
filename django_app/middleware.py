import logging
 
logger = logging.getLogger(__name__)

# Logs the request method and path.
# Middleware class must implement __init__ and __call__

#use curl -I http://127.0.1:8000/polls/ to see the log
class LogRequestMiddleware:

    def __init__(self, get_response): # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request): #  Code executed for each request before the view is called.
        # Code executed for each request before the view is called.
        logger.info(f"Request Method: {request.method}, Path: {request.path}")

        response = self.get_response(request)

        # Code executed for each response after the view is called.
        return response
    
# use curl -I http://127.0.0.1:8000/polls/ to see the custom header
class CustomHeaderMiddleware:

    def __init__(self, get_response):
        print('CustomHeader __init__')
        self.get_response = get_response

    def __call__(self, request):
        print('CustomHeader __call__ ')
        response = self.get_response(request)
        response['X-Custom-Header'] = 'My Custom Value'
        return response
    
