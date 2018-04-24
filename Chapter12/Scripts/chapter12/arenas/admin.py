from django.contrib.gis import admin
from .models import US_States, Counties, Arenas, Districts


admin.site.register(US_States, admin.GeoModelAdmin)
admin.site.register(Counties, admin.GeoModelAdmin)
admin.site.register(Arenas, admin.GeoModelAdmin)
admin.site.register(Districts, admin.GeoModelAdmin)
