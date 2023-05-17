import json
import django.shortcuts as shortcuts
from django.utils import timezone
from .models import UserLog


def redirect(request):
    if request.method == 'GET' and 'next' in request.GET:
        redirect_to = request.GET.get('next')
    else:
        redirect_to = '/'
    import logging
    logging.error(request.user)
    logging.error(request.user.username)
    log = UserLog(
        timestamp=int(timezone.now().timestamp()),
        username=request.user.username if request.user.is_authenticated else None,
        action=UserLog.Action.GO_TO,
        action_value=json.dumps({'redirect_to': redirect_to}),
    )
    log.save()
    return shortcuts.redirect(redirect_to)
