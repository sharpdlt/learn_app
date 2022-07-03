from django.shortcuts import get_object_or_404, render
from django.core.signing import BadSignature

from .utilities import signer
from .models import Profile


def index(request):
    context = {}
    return render(request, 'main/index.html', context)


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(Profile, username=username)

    if user.is_activated:
        template = 'main/index.html'
    else:
        print('activate')
        template = 'main/index.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)