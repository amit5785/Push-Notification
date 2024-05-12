from django.contrib import admin

# Register your models here.

from django import forms
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.urls import path
from django.http import HttpResponseRedirect

class sendNotificationForm(forms.Form):
  message = forms.CharField(label = 'Notification message', max_length = 200)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
  add_form_template = "admin/custom_add_form.html"
  
  def add_view(self, request, form_url = '', extra_contxt = None):
    if request.method == 'POST':
      form = sendNotificationForm(request.POST)
      if form.is_valid():
        message = form.cleaned_data['message']

        notification = Notification.objects.create(message = message)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
          "notifications",
          {
              "type": "send_notification",
              "message": message
          }
        )
        return HttpResponseRedirect(f"../{notification.pk}/")
    else:
      form = sendNotificationForm()

    context = self.get_changeform_initial_data(request = request)
    context['form'] = form
    return super().add_view(request = request, form_url = form_url, extra_context = context)
  
  def get_urls(self):
    urls = super().get_urls()
    custom_url = [
        path("send-notification/", self.admin_site.admin_view(self.add_view), name="send-notification"),
    ]
    return custom_url + urls