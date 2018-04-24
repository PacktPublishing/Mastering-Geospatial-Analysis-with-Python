from django.contrib.gis.db import models


class Arenas(models.Model):
    sector = models.CharField(max_length=30)
    subsector = models.CharField(max_length=22)
    primary_ty = models.CharField(max_length=45)
    date_creat = models.CharField(max_length=15)
    date_modif = models.CharField(max_length=24)
    comp_affil = models.CharField(max_length=29)
    name1 = models.CharField(max_length=66)
    name2 = models.CharField(max_length=26)
    name3 = models.CharField(max_length=10)
    address1 = models.CharField(max_length=29)
    address2 = models.CharField(max_length=20)
    po_box = models.CharField(max_length=24)
    po_zip = models.CharField(max_length=24)
    city = models.CharField(max_length=14)
    state = models.CharField(max_length=4)
    zip = models.CharField(max_length=6)
    zip_4 = models.CharField(max_length=12)
    county = models.CharField(max_length=19)
    hsip_aoi = models.CharField(max_length=23)
    fema_regio = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    reliabilit = models.CharField(max_length=16)
    coorsource = models.CharField(max_length=14)
    comments_1 = models.CharField(max_length=93)
    conference = models.CharField(max_length=16)
    division = models.CharField(max_length=16)
    capacity = models.FloatField()
    team = models.CharField(max_length=30)
    geom = models.PointField(srid=4326)


# Auto-generated `LayerMapping` dictionary for Arenas model
arenas_mapping = {
    'sector': 'SECTOR',
    'subsector': 'SUBSECTOR',
    'primary_ty': 'PRIMARY_TY',
    'date_creat': 'DATE_CREAT',
    'date_modif': 'DATE_MODIF',
    'comp_affil': 'COMP_AFFIL',
    'name1': 'NAME1',
    'name2': 'NAME2',
    'name3': 'NAME3',
    'address1': 'ADDRESS1',
    'address2': 'ADDRESS2',
    'po_box': 'PO_BOX',
    'po_zip': 'PO_ZIP',
    'city': 'CITY',
    'state': 'STATE',
    'zip': 'ZIP',
    'zip_4': 'ZIP_4',
    'county': 'COUNTY',
    'hsip_aoi': 'HSIP_AOI',
    'fema_regio': 'FEMA_REGIO',
    'latitude': 'LATITUDE',
    'longitude': 'LONGITUDE',
    'reliabilit': 'RELIABILIT',
    'coorsource': 'COORSOURCE',
    'comments_1': 'COMMENTS_1',
    'conference': 'CONFERENCE',
    'division': 'DIVISION',
    'capacity': 'CAPACITY',
    'team': 'TEAM',
    'geom': 'POINT',
}

class US_States(models.Model):
    stfips = models.CharField(max_length=2)
    state = models.CharField(max_length=66)
    stpostal = models.CharField(max_length=2)
    version = models.CharField(max_length=2)
    dotregion = models.IntegerField()
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)


# Auto-generated `LayerMapping` dictionary for US_States model
us_states_mapping = {
    'stfips': 'STFIPS',
    'state': 'STATE',
    'stpostal': 'STPOSTAL',
    'version': 'VERSION',
    'dotregion': 'DotRegion',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'geom': 'MULTIPOLYGON',
}
class Counties(models.Model):
    stfips = models.CharField(max_length=2)
    ctfips = models.CharField(max_length=5)
    state = models.CharField(max_length=66)
    county = models.CharField(max_length=66)
    version = models.CharField(max_length=2)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)


# Auto-generated `LayerMapping` dictionary for Counties model
counties_mapping = {
    'stfips': 'STFIPS',
    'ctfips': 'CTFIPS',
    'state': 'STATE',
    'county': 'COUNTY',
    'version': 'VERSION',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'geom': 'MULTIPOLYGON',
}




class Districts(models.Model):
    district = models.CharField(max_length=2)
    name = models.CharField(max_length=25)
    party = models.CharField(max_length=19)
    state = models.CharField(max_length=2)
    stfips = models.CharField(max_length=2)
    version = models.CharField(max_length=2)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)


# Auto-generated `LayerMapping` dictionary for Districts model
districts_mapping = {
    'district': 'DISTRICT',
    'name': 'NAME',
    'party': 'PARTY',
    'state': 'STATE',
    'stfips': 'STFIPS',
    'version': 'VERSION',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'geom': 'MULTIPOLYGON',
}
