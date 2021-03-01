from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.views import generic
from django.utils import timezone


from .models import Guild, Description
from django.urls import reverse


class IndexView(generic.ListView):

    template_name = 'guilds/index.html'
    context_object_name = 'guilds'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Guild.objects.filter(creation_date__lte=timezone.now()).order_by('-creation_date')[:5]

class DetailView(generic.DetailView):

    model = Guild
    template_name = 'guilds/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Guild.objects.filter(creation_date__lte=timezone.now())

class ResultsView(generic.DetailView):

    model = Guild
    template_name = 'guilds/results.html'


def vote(request, guild_id):
    guild = get_object_or_404(Guild, pk=guild_id)
    try:
        selected_description = guild.description_set.get(pk=request.POST['desc'])
    except (KeyError, Description.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'guilds/detail.html', {
            'guild': guild,
            'error_message': "You didn't select a Description.",
        })
    else:
        selected_description.votes += 1
        selected_description.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('guilds:results', args=(guild_id,)))



