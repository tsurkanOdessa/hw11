from django.contrib import admin
from .models import Task, SubTask, Category

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

@admin.action(description='Mark as Done')
def mark_as_done(modeladmin, request, queryset):
    queryset.update(is_done=True)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]
    list_display = ('short_title', 'created_at')  # 'short_title' — кастомный метод

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'is_done')
    actions = [mark_as_done]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)