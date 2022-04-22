from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register/',views.Register),
    path('login/',csrf_exempt(views.Login)),
    path('user/',views.UserData),
    path('logout/',csrf_exempt(views.Logout)),
    path('details/',views.GetAccountDetails),
    path('loans/',views.GetLoanDetails)
]
