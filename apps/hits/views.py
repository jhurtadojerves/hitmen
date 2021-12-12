# Django
from django.core.exceptions import PermissionDenied

from django.views.generic import UpdateView, DetailView
from django.contrib.auth.models import Permission
from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView
