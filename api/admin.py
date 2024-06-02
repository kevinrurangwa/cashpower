from django.contrib import admin
from .models import User, Request, Upload, RequestHandle, Dispense

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'user_type', 'phone_number')
    list_filter = ('user_type',)
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    readonly_fields = ('last_login', 'date_joined', 'password')

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'requested_service', 'status', 'requested_on', 'updated_at')
    list_filter = ('status', 'requested_on', 'updated_at')
    search_fields = ('client__email', 'requested_service', 'status')
    readonly_fields = ('requested_on', 'updated_at')

@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'type', 'file')
    search_fields = ('request__id', 'type')

@admin.register(RequestHandle)
class RequestHandleAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'handler', 'handled_on')
    list_filter = ('handled_on',)
    search_fields = ('request__id', 'handler__email')
    readonly_fields = ('handled_on',)

@admin.register(Dispense)
class DispenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'cash_power', 'done_at', 'user', 'address')
    list_filter = ('done_at',)
    search_fields = ('request__id', 'cash_power', 'user__email')
    readonly_fields = ('done_at',)
