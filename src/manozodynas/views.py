from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import LoginForm
from django.contrib.auth import login
from django.views.generic import CreateView, ListView
from manozodynas.models import Word, Translation

def index_view(request):
    return render(request, 'manozodynas/index.html', {})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = LoginForm()
    #import ipdb; ipdb.set_trace()
    return render(request, 'manozodynas/login.html', {'form':form})


class WordAdd(CreateView):
    model = Word
    success_url = "/"


class WordList(ListView):
    model = Word


class TranslationAdd(CreateView):
    model = Translation
    fields = ['translation']
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super(TranslationAdd, self).get_context_data(**kwargs)
        context['word'] = get_object_or_404(Word, id=self.kwargs.get('id'))
        return context

    def form_valid(self, form):
        word = get_object_or_404(Word, id=self.kwargs.get('id'))
        form.instance.word = word
        return super(TranslationAdd, self).form_valid(form)
