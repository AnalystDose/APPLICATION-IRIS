from django.contrib import admin
from .models import Stock
# from import_export.admin import ImportExportModelAdmin
#
#
# class StockAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     ...


admin.site.register(Stock)
