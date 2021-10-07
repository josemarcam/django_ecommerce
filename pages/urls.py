from django.urls.conf import path
from pages.views import AboutPageView, HomePageView

app_name = "pages"

urlpatterns = [
    path("about/",AboutPageView.as_view(),name="about"),
    path("", HomePageView.as_view(),name="home" ),
]
