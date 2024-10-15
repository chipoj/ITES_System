from django.http import HttpResponse
import csv

def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="table_data.csv"'
    
    writer = csv.writer(response)
    model = queryset.model
    fields = [field.name for field in model._meta.fields]
    
    writer.writerow(fields)
    for obj in queryset:
        writer.writerow([str(getattr(obj, field)) for field in fields])
    
    return response

export_as_csv.short_description = 'Export selected as CSV'