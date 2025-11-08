from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.
@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name='public')
    chat_messages = chat_group.chat_messages.all()[:30]
    # {'chat_messages': chat_messages}
    return render(request, 'rtchat/chat.html', {'chat_messages': chat_messages})
