from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
import channels
from .models import TV
from content.models import Content, Group, Media
from .serializers import TVSerializer

class TvConsumer(WebsocketConsumer):
    def connect(self):
        self.tv = str(self.scope['url_route']['kwargs']['tv'])
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.tv,
            self.channel_name
        )
        self.accept()
    
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.tv,
            self.channel_name
        )

    # Receive message from room group
    def change_message(self, event):
        message = event['message']
        data = event.get('data', None)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'data':data
        }))

def send_message(tv):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(tv.pk), {"type": "change_message", "message": "mudou"}
    )
    
@receiver(post_save, sender=TV)
def tv_post_update(sender, instance, created, **kwargs):
    send_message(instance)

@receiver(post_save, sender=Media)
def media_post_update(sender, instance, created,**kwargs):
    tvs = TV.objects.filter(group__contents=instance)
    for tv in tvs:
        send_message(tv)

@receiver(post_save, sender=Content)
def content_post_update(sender, instance, created,**kwargs):
    tvs = TV.objects.filter(group=instance.group)
    for tv in tvs:
        send_message(tv)


@receiver(post_save, sender=Group)
def group_post_update(sender, instance, created,**kwargs):
    tvs = instance.tvs.all()
    for tv in tvs:
        send_message(tv)