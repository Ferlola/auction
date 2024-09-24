from django.contrib import admin

from src.bids.models import BidsHistory
from src.bids.models import BidsWinner

admin.site.register(BidsHistory)
admin.site.register(BidsWinner)
