from channels.generic.websocket import AsyncWebsocketConsumer
from django.template import Context, Template
import json

class NotificationConsumer(AsyncWebsocketConsumer):
  
  async def connect(self):
    await self.accept()
    await self.channel_layer.group_add('notifications', self.channel_name)
    return
  
  async def disconnect(self, close_code):
    await self.channel_layer.group_discard('notifications', self.channel_name)
    return

  async def send_notification(self, event):
    message = event["message"]

    template =  Template('<div class = "notification"><p>{{message}}</p></div>')
    context = Context({'message' : message})
    rendered_notifcation = template.render(context = context)
    await self.send(
      text_data = json.dumps({
        "type" : "notification",
        "message" : rendered_notifcation
      })
    )

