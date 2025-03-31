from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

    class Meta:
        app_label = 'iot'

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    activity_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} - {self.activity_text}"
    

class Report(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=10, choices=[('doc', 'Document'), ('sql', 'SQL'), ('url', 'URL')])
    last_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)  # True (Green) / False (Red)

    def __str__(self):
        return self.name
    
class TableList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    
from django.db import models

class UserGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    level = models.IntegerField()
    status = models.CharField(max_length=50, choices=[("Enable", "Enable"), ("Disable", "Disable")])
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


from django.db import models

class SubMenu(models.Model):
    menu_id = models.CharField(max_length=100, unique=True)
    menu_item_desc = models.CharField(max_length=255)
    item_seq = models.PositiveIntegerField()
    module_name = models.CharField(max_length=100)
    main_menu_action_name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=[('Enable', 'Enable'), ('Disable', 'Disable')])

    def __str__(self):
        return self.menu_item_desc

from django.db import models

class MainMenu(models.Model):
    menu_name = models.CharField(max_length=100, unique=True)
    menu_url = models.CharField(max_length=200, blank=True, null=True)
    display_order = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.menu_name

from django.db import models

class Menu(models.Model):
    menuId = models.CharField(max_length=100)
    menuItemDesc = models.CharField(max_length=255)
    itemSeq = models.IntegerField()
    moduleName = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    main_menu_action_name = models.CharField(max_length=255)
    main_menu_icon_name = models.CharField(max_length=255)

    def __str__(self):
        return self.menuItemDesc