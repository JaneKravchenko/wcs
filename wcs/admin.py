from django.contrib import admin


from .models import Shapefile, Attribute, Feature, AttributeValue

admin.site.register(Shapefile)
admin.site.register(Attribute)
admin.site.register(Feature)
admin.site.register(AttributeValue)