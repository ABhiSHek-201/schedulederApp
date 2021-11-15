from django.urls import path
from .views import BorrowerView,LoanView

urlpatterns = [
    path('borrowers',BorrowerView.as_view()),
    path('loans',LoanView.as_view()),
]
