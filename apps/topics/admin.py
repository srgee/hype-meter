from django.contrib import admin
from .models import Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'score', 'get_status', 'updated_at', 'is_data_stale')
    
    list_filter = ('score', 'updated_at')
    
    # Search bar to find keywords quickly
    search_fields = ('name',)
    
    readonly_fields = ('created_at', 'updated_at', 'history_data')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'score')
        }),
        ('Metadatos y Caché', {
            'fields': ('history_data', 'created_at', 'updated_at'),
            'classes': ('collapse',),  # Los oculta por defecto para limpiar la interfaz
        }),
    )

    @admin.display(description='Status')
    def get_status(self, obj):
        '''Shows status label.'''
        return obj.status_label

    @admin.display(description='¿Obsoleto?', boolean=True)
    def is_data_stale(self, obj):
        '''Shows whether data is stale or current.'''
        return obj.is_stale()