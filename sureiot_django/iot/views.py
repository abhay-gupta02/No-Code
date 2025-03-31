from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project, Activity, Report

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Generate JWT token upon successful authentication.
            payload = {
                'user_id': user.id,
                'username': user.username,
                'exp': datetime.utcnow() + timedelta(hours=1),  # Token expires in 1 hour.
                'iat': datetime.utcnow(),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            # Log the user in using Django's login system.
            login(request, user)
            response = redirect('dashboard')
            response.set_cookie('jwt', token, httponly=True, samesite='Lax')  # Store JWT in HttpOnly cookie
            return response
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'iot/login.html')

@login_required
def dashboard_view(request):
    projects = Project.objects.all()
    project_count = projects.count()
    activities = Activity.objects.order_by('-created_at')[:10]

    barChartLabels = [project.name for project in projects]
    barChartData = [1 for _ in projects]  # Dummy metric

    lineChartLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    lineChartData = [project_count, project_count + 2, project_count + 3, project_count + 1, project_count + 5]

    context = {
        'dashboardModel': [{'name': 'Index', 'charttitle': 'Sample Chart', 'key': 'value'}],
        'dashboardChartData': [
            {'name': 'Bar Chart', 'charttitle': 'Projects Bar Chart', 'featchData': {'barChartData': barChartData, 'barChartLabels': barChartLabels}},
            {'name': 'Line Chart', 'charttitle': 'Projects Line Chart', 'featchData': {'chartData': lineChartData, 'chartLabels': lineChartLabels}},
        ],
        'projects': projects,
        'activities': activities,
        'project_count': project_count,
    }
    return render(request, 'iot/dashboard.html', context)

def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('jwt')  # Remove JWT cookie
    return response

@login_required
def reports_list(request):
    reports = Report.objects.all()
    return render(request, 'iot/reports_list.html', {'reports': reports})

@login_required
def report_builder_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        query = request.POST.get("query")

        if name and query:
            Report.objects.create(name=name, description=query)
            messages.success(request, "Report saved successfully!")
            return redirect("reports_list")

    return render(request, "iot/report_builder.html")

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        projects = Project.objects.all()
        activities = Activity.objects.order_by('-created_at')[:10]

        project_count = projects.count()
        bar_chart_labels = [project.name for project in projects]
        bar_chart_data = [1 for _ in projects]

        line_chart_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
        line_chart_data = [project_count, project_count + 2, project_count + 3, project_count + 1, project_count + 5]

        context = {
            'dashboardModel': [{'name': 'Index', 'charttitle': 'Sample Chart', 'key': 'value'}],
            'dashboardChartData': [
                {'name': 'Bar Chart', 'charttitle': 'Projects Bar Chart', 'featchData': {'barChartData': bar_chart_data, 'barChartLabels': bar_chart_labels}},
                {'name': 'Line Chart', 'charttitle': 'Projects Line Chart', 'featchData': {'chartData': line_chart_data, 'chartLabels': line_chart_labels}},
            ],
            'projects': [project.name for project in projects],
            'activities': [{'activity_text': act.activity_text, 'created_at': act.created_at} for act in activities],
            'project_count': project_count,
        }
        return Response(context)


from django.shortcuts import render
from .models import Report
from django.views.decorators.csrf import csrf_exempt

def reports_list(request):
    reports = Report.objects.all()
    return render(request, 'iot/reports_list.html', {'reports': reports})


@csrf_exempt
def report_runner_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        is_active = request.POST.get('is_active') == 'on'
        folder_name = request.POST.get('folder_name')
        Report.objects.create(name=name, description=description, is_active=is_active, folder_name=folder_name)
        return redirect('reports_list')
    return render(request, 'report_runner_add.html')

def report_edit(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        report.name = request.POST.get('name')
        report.description = request.POST.get('description')
        report.is_active = request.POST.get('is_active') == 'on'
        report.folder_name = request.POST.get('folder_name')
        report.save()
        return redirect('reports_list')
    return render(request, 'report_runner_add.html', {'report': report})

def report_delete(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.delete()
    return redirect('reports_list')

from django.shortcuts import render
from .models import TableList

def sql_worksheet(request):
    tables = TableList.objects.all()
    return render(request, 'iot/sql_worksheet.html', {'tables': tables})

from django.shortcuts import render

from django.shortcuts import render
from django.http import JsonResponse

def report_setup(request):
    if request.method == 'POST':
        url = request.POST.get('get_url')
        list_choice = request.POST.get('list_choice')
        params = request.POST.get('params')
        include_date_filter = request.POST.get('include_date_filter') == 'on'
        # Process the data as needed
        response_data = {
            'status': 'success',
            'message': 'Report setup updated successfully!'
        }
        return JsonResponse(response_data)
    return render(request, 'iot/report_setup.html')

def get_standard_parameters(request):
    # Sample data for standard parameters
    standard_parameters = [
        'pincode', 'mobno', 'address', 'name', 'id', 'email'
    ]
    return JsonResponse(standard_parameters, safe=False)


def projects_list(request):
    return render(request, 'projects_list.html')  # Ensure this template exists


def tasks_list(request):
    return render(request, 'tasks_list.html')  # Ensure this template exists




def settings_view(request):
    return render(request, 'settings.html')  # Make sure this template exists


from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .models import UserGroup  # Ensure this matches your model name

def user_maintenance(request):
    groups = UserGroup.objects.all()  # Fetch all groups from the database
    return render(request, 'iot/user_maintenance.html', {'groups': groups})



def user_maintenance_add(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        level = request.POST.get("level")
        status = request.POST.get("status")

        UserGroup.objects.create(name=name, description=description, level=level, status=status)
        return redirect("user_maintenance")

    return render(request, "iot/user_maintenance_add.html")

def user_maintenance_edit(request, group_id):
    group = get_object_or_404(UserGroup, id=group_id)

    if request.method == "POST":
        group.name = request.POST.get("name")
        group.description = request.POST.get("description")
        group.level = request.POST.get("level")
        group.status = request.POST.get("status")
        group.save()
        return redirect("user_maintenance")

    return render(request, "iot/user_maintenance_edit.html", {"group": group})

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import UserGroup

def delete_user_group(request, group_id):
    if request.method == "POST":
        group = get_object_or_404(UserGroup, id=group_id)
        group.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


from django.shortcuts import render, redirect, get_object_or_404
from .models import SubMenu
from django.http import JsonResponse

def menu_maintenance_list(request):
    sub_menus = SubMenu.objects.all()
    return render(request, 'iot/menu_maintenance.html', {'sub_menus': sub_menus})

def add_sub_menu(request):
    if request.method == 'POST':
        menu_id = request.POST['menuId']
        menu_item_desc = request.POST['menuItemDesc']
        item_seq = request.POST['itemSeq']
        module_name = request.POST['moduleName']
        main_menu_action_name = request.POST['main_menu_action_name']
        status = request.POST['status']

        SubMenu.objects.create(
            menu_id=menu_id,
            menu_item_desc=menu_item_desc,
            item_seq=item_seq,
            module_name=module_name,
            main_menu_action_name=main_menu_action_name,
            status=status
        )
        return redirect('menu_maintenance_list')

def edit_sub_menu(request, id):
    submenu = get_object_or_404(SubMenu, id=id)
    if request.method == 'POST':
        submenu.menu_item_desc = request.POST['menuItemDesc']
        submenu.item_seq = request.POST['itemSeq']
        submenu.module_name = request.POST['moduleName']
        submenu.main_menu_action_name = request.POST['main_menu_action_name']
        submenu.status = request.POST['status']
        submenu.save()
        return redirect('menu_maintenance_list')
    return render(request, 'edit_sub_menu.html', {'submenu': submenu})

def delete_sub_menu(request, id):
    submenu = get_object_or_404(SubMenu, id=id)
    submenu.delete()
    return redirect('menu_maintenance_list')


from django.shortcuts import render, redirect, get_object_or_404
from .models import MainMenu
from django.http import JsonResponse

import json  # Add this import
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Menu  # Replace with your actual model

@csrf_exempt
def menus(request):
    if request.method == 'GET':
        # Fetch data from the database
        menus = Menu.objects.all().values(
            'menuId', 'menuItemDesc', 'itemSeq', 'moduleName', 'status', 'main_menu_action_name', 'main_menu_icon_name'
        )
        data = list(menus)  # Convert queryset to a list of dictionaries
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON data from the request body
        # Save data to the database
        # Example: Menu.objects.create(**data)
        return JsonResponse({"status": "success"})
    elif request.method == 'DELETE':
        # Delete data from the database
        # Example: Menu.objects.filter(id=pk).delete()
        return JsonResponse({"status": "success"})
def main_menu_list(request):
    menus = MainMenu.objects.all().order_by('display_order')
    return render(request, 'iot/main_menu_maintenance.html', {'menus': menus})

def add_main_menu(request):
    if request.method == 'POST':
        menu_name = request.POST.get('menu_name')
        menu_url = request.POST.get('menu_url')
        display_order = request.POST.get('display_order')
        is_active = request.POST.get('is_active') == 'on'
        
        MainMenu.objects.create(
            menu_name=menu_name,
            menu_url=menu_url,
            display_order=display_order,
            is_active=is_active
        )
        return redirect('main_menu_list')
    
def main_menu_add(request):
    if request.method == 'POST':
        # Handle form submission and save the new menu item
        name = request.POST.get('name')
        url = request.POST.get('url')
        icon = request.POST.get('icon')
        sequence = request.POST.get('sequence')
        
        MainMenu.objects.create(name=name, url=url, icon=icon, sequence=sequence)
        return redirect('iot:main_menu_list')
    
    return render(request, 'iot/main_menu_add.html')

def delete_main_menu(request, menu_id):
    if request.method == 'GET' and request.is_ajax():
        menu = get_object_or_404(MainMenu, id=menu_id)
        menu.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def edit_main_menu(request, menu_id):
    menu = get_object_or_404(MainMenu, id=menu_id)
    if request.method == 'POST':
        menu.menu_name = request.POST.get('menu_name')
        menu.menu_url = request.POST.get('menu_url')
        menu.display_order = request.POST.get('display_order')
        menu.is_active = request.POST.get('is_active') == 'on'
        menu.save()
        return redirect('main_menu_list')
    return render(request, 'iot/edit_main_menu.html', {'menu': menu})
