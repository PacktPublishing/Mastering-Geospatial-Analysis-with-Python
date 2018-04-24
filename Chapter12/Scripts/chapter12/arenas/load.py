import os
from django.contrib.gis.utils import LayerMapping
from .models import US_States, Counties, Arenas, Districts

us_states_mapping = {
    'stfips' : 'STFIPS',
    'state' : 'STATE',
    'stpostal' : 'STPOSTAL',
    'version' : 'VERSION',
    'dotregion' : 'DotRegion',
    'shape_leng' : 'Shape_Leng',
    'shape_area' : 'Shape_Area',
    'geom' : 'MULTIPOLYGON',
}




states_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'US_States.shp'),
)


us_counties_mapping = {
    'stfips' : 'STFIPS',
    'ctfips' : 'CTFIPS',
    'state' : 'STATE',
    'county' : 'COUNTY',
    'version' : 'VERSION',
    'shape_leng' : 'Shape_Leng',
    'shape_area' : 'Shape_Area',
    'geom' : 'MULTIPOLYGON',
}

counties_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'US_County_Boundaries.shp'),
)


districts_mapping = {
    'district' : 'DISTRICT',
    'name' : 'NAME',
    'party' : 'PARTY',
    'state' : 'STATE',
    'stfips' : 'STFIPS',
    'version' : 'VERSION',
    'shape_leng' : 'Shape_Leng',
    'shape_area' : 'Shape_Area',
    'geom' : 'MULTIPOLYGON',
}

districts_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'Congressional_Districts.shp'),
)


arenas_mapping = {
    'sector' : 'SECTOR',
    'subsector' : 'SUBSECTOR',
    'primary_ty' : 'PRIMARY_TY',
    'date_creat' : 'DATE_CREAT',
    'date_modif' : 'DATE_MODIF',
    'comp_affil' : 'COMP_AFFIL',
    'name1' : 'NAME1',
    'name2' : 'NAME2',
    'name3' : 'NAME3',
    'address1' : 'ADDRESS1',
    'address2' : 'ADDRESS2',
    'po_box' : 'PO_BOX',
    'po_zip' : 'PO_ZIP',
    'city' : 'CITY',
    'state' : 'STATE',
    'zip' : 'ZIP',
    'zip_4' : 'ZIP_4',
    'county' : 'COUNTY',
    'hsip_aoi' : 'HSIP_AOI',
    'fema_regio' : 'FEMA_REGIO',
    'latitude' : 'LATITUDE',
    'longitude' : 'LONGITUDE',
    'reliabilit' : 'RELIABILIT',
    'coorsource' : 'COORSOURCE',
    'comments_1' : 'COMMENTS_1',
    'conference' : 'CONFERENCE',
    'division' : 'DIVISION',
    'capacity' : 'CAPACITY',
    'team' : 'TEAM',
    'geom' : 'POINT',
}

arenas_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'Arenas_NBA.shp'),
)


def run(verbose=True):
##    lm = LayerMapping(
##        US_States, states_shp, us_states_mapping,
##        transform=False, encoding='iso-8859-1',
##    )
####    lm.save(strict=True, verbose=verbose)
    lm = LayerMapping(
        Counties, counties_shp, us_counties_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=True, verbose=verbose)
    lm = LayerMapping(
        Districts, districts_shp, districts_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=True, verbose=verbose)
    lm = LayerMapping(
        Arenas, arenas_shp, arenas_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=True, verbose=verbose)
