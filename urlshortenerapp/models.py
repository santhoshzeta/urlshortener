from django.db import models
from datetime import datetime, timedelta
from urllib.parse import urlparse
from collections import Counter
import logging

log = logging.getLogger(__name__)


class UrlManager(models.Manager):

    def getorcreatelongurl(self, longurl):
        """Checks if an url exists in the DB,
            if it doesn't exists create a new record,
            else pass the value from DB
        """
        if(isinstance(longurl, str)):
            url, created = Url.objects.get_or_create(longurl=longurl)
            log.info(f"{longurl} created:{created}")
            return url
        else:
            raise ValueError("longurl must be a string")

    def gettopdomains(self, lookbackdays=30, topnum=10):
        """Retrieves top domains based on the lookback days"""
        lookbackstarttime = datetime.today() - timedelta(days=lookbackdays)
        items = Url.objects.filter(createddatetime__gte=lookbackstarttime).order_by('createddatetime')
        basedomains = []
        for url in items:
            hostname = urlparse(url.longurl).hostname
            if isinstance(hostname, str):
                basedomains.append(hostname.replace("www.", ""))
        return list(Counter(basedomains).most_common(topnum))


class Url(models.Model):
    longurl = models.CharField(db_column='long_url', max_length=1024, db_index=True)
    createddatetime = models.DateTimeField(auto_now_add=True, db_column='created_datetime', db_index=True)

    objects = UrlManager()      # Custom Manager

    def __str__(self):
        return str(self.longurl)

    class Meta:
        db_table = "url"


class UrlVisit(models.Model):
    url = models.ForeignKey(Url)
    visitdatetime = models.DateTimeField(auto_now_add=True, db_column='visited_datetime')

    class Meta:
        db_table = "url_visit"
