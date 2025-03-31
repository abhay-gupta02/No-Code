from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import reports_list, report_builder_view
from rest_framework.authtoken.views import obtain_auth_token
from .views import user_maintenance, user_maintenance_add, user_maintenance_edit
from django.shortcuts import render, get_object_or_404, redirect
from .views import delete_user_group
from .views import report_setup
from .views import report_setup, get_standard_parameters



urlpatterns = [
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Alternative token-based authentication 
    path('api/auth-token/', obtain_auth_token, name='api_auth_token'),

    # Authentication & Dashboard
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Reports Section
   # path('reports/', reports_list, name='reports_list'),
    path('reports/', views.reports_list, name='reports_list'),  
    path('reports/builder/', report_builder_view, name='report_builder'),
    path('report-runner/add/', views.report_runner_add, name='report_runner_add'),
    path('report/edit/<int:pk>/', views.report_edit, name='report_edit'),
    path('report/delete/<int:pk>/', views.report_delete, name='report_delete'),
    path('sql-worksheet/', views.sql_worksheet, name='sql_worksheet'),
    path('report-setup/', report_setup, name='report_setup'),
    path('report-setup/standard-parameters/', get_standard_parameters, name='get_standard_parameters'),

    path('projects/', views.projects_list, name='projects_list'),
    path('tasks/', views.tasks_list, name='tasks_list'),
    path('settings/', views.settings_view, name='settings'),

    path("user-maintenance/", user_maintenance, name="user_maintenance"),
    path("user-maintenance/add/", user_maintenance_add, name="user_maintenance_add"),
    path("user-maintenance/edit/<int:group_id>/", user_maintenance_edit, name="user_maintenance_edit"),
    path("reports/user-maintenance/delete/<int:group_id>/", delete_user_group, name="user_maintenance_delete"),


    # Favicon Handling
    path('favicon.ico', lambda request: redirect('/static/images/favicon.ico', permanent=True)),
    #menu 1
    path('menu-maintenance/', views.menu_maintenance_list, name='menu_maintenance_list'),
    path('menu-maintenance/add/', views.add_sub_menu, name='add_sub_menu'),
    path('menu-maintenance/edit/<int:id>/', views.edit_sub_menu, name='edit_sub_menu'),
    path('menu-maintenance/delete/<int:id>/', views.delete_sub_menu, name='delete_sub_menu'),

    #menu
    path('main-menu/', views.main_menu_list, name='main_menu_list'),
    path('main-menu/add/', views.add_main_menu, name='add_main_menu'),
    path('main-menu/add/', views.main_menu_add, name='main_menu_add'),
    path('main-menu/edit/<int:menu_id>/', views.edit_main_menu, name='edit_main_menu'),
    path('main-menu/delete/<int:menu_id>/', views.delete_main_menu, name='main_menu_delete'),

    path('api/menus/', views.menus),
    path('api/menus/<int:pk>/', views.menus),
]
