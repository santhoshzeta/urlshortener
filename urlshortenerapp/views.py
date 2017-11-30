from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .models import Url, UrlVisit
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .utils import gethashkeyfromurl, encode, decode
from django.core.exceptions import DoesNotExist
from django.http import HttpResponseBadRequest
import logging

log = logging.getLogger(__name__)


def home(request):
    """ Default handler for urlshortener """
    return render(request, 'urlshortenerapp/home.html', {})


@csrf_exempt
def shorten(request):
    """ Check if the long url exists
            If Yes - generate hashcode
            If No - adds to DB and generate hashcode
        Constructs shorten url using the generated hashcode"""

    if request.method == "POST" and request.is_ajax():
        longurl = request.POST.get('longurl')
        log.info(f"Received request to shorten url: {longurl}")
        if longurl:
            url = Url.objects.getorcreatelongurl(longurl)
            shorturl = request.build_absolute_uri('/')+encode(url.id)
            log.info(f"Shortened url: {shorturl}")
        else:
            return HttpResponseBadRequest()
    return JsonResponse({'shorturl': shorturl})


def topdomains(request):
    """ Retrieves the popular domains in the last 30 days"""
    context = {'domains': Url.objects.gettopdomains(30, 10)}
    return render(request, 'urlshortenerapp/topdomains.html', context)


def last100urls(request):
    """ Retrieves the last 100 shortened urls """
    last100urls = Url.objects.all().order_by('-id')[:100]
    log.debug(f"List of last 100 urls: {str(last100urls)}")
    context = {'last100urls': last100urls}
    return render(request, 'urlshortenerapp/last100urls.html', context)


def urlvisitstats(request):
    return render(request, 'urlshortenerapp/urlvisitstats.html', {})


@csrf_exempt
def retrievestats(request):
    """ Retrieves visit count for a given short url """
    if request.method == "POST" and request.is_ajax():
        shorturl = request.POST.get('shorturl')
        if shorturl:
            log.info(f"Retrieving stats for {shorturl}")
            key = gethashkeyfromurl(shorturl)
            urlid = decode(key)
            try:
                Url.objects.get(id=urlid)
                urlcount = UrlVisit.objects.filter(url=urlid).count()
                context = {'success': True, 'count': urlcount}
            except ObjectDoesNotExist as e:
                log.warn(e, exc_info=True)
                context = {'success': False}
        else:
            log.warn("Invalid input, url missing")
            context = {'success': False}
        return JsonResponse(context)


def redirect(request):
    """ Redirects short url to long and update visit stat to UrlVisit table"""
    relativeurl = request.get_full_path()
    log.debug(f'Redirect request received for: {relativeurl}')
    if relativeurl.startswith('/'):
        relativeurl = relativeurl[1:len(relativeurl)]
    urlid = decode(relativeurl)
    try:
        url = Url.objects.get(id=urlid)
    except DoesNotExist:
        longurl = request.build_absolute_uri('/')
    else:
        if(not url.longurl.startswith('http')):
            longurl = 'http://'+url.longurl
        else:
            longurl = url.longurl
        urlvisit = UrlVisit(url=url)
        urlvisit.save()
        log.debug(f'Url visit saved successfully with the id:{urlvisit.id}')
    return HttpResponseRedirect(longurl)
