from django.core.exceptions import PermissionDenied
from .models import Auction

def user_is_auction_author(function):
    def wrap(request, *args, **kwargs):
        auction = Auction.objects.get(pk=kwargs['pk'])
        if auction.lister == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

