from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    url(r'^login/$',
        LoginView.as_view(template_name='login.html'),
        name='login'),
    url(r'^logout/$',
        LogoutView.as_view(next_page=reverse_lazy('login')),
        name='logout')
]
