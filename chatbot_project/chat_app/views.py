from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
import openai

@csrf_exempt


def ask(request):
    openai.api_key = '#取得したAPIキー#'

    user_message = request.POST.get('message')
    conversation = request.session.get('conversation', [])
    conversation.append(user_message)

    prompt = " ".join(conversation)

    response = openai.Completion.create(model="#作成したモデル#", prompt=prompt, max_tokens=100, n=1, stop=None, temperature=0.3,)

    bot_response = response.choices[0].text.strip()
    conversation.append(bot_response)
    request.session['conversation'] = conversation

    if len(conversation) > 15:
        call_command('flush',interactive=False)
        call_command('migrate')

    return JsonResponse({'message': bot_response})

def chat_view(request):
    return render(request, 'chat.html')
