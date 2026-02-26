from django.utils.timezone import now

class VisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Visit at:", now())
        response = self.get_response(request)
        return response