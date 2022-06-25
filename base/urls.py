from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name="home"),
    path('login',views.login,name="login"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('addExpense',views.addExpense,name="addExpense"),
    path('addBank',views.addBank,name="addBank"),
    path('displayExpense',views.displayExpense,name="displayExpense"),
    path('deleteTransaction/<int:tid>',views.deleteTransaction,name="deleteTransaction"),
    path('logout',views.logout,name="logout")
]
