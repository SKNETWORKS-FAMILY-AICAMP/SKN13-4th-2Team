from django.contrib import admin
from .models import Profile, Playlist, ListeningHistory

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'avatar')
    search_fields = ('user__username', 'nickname')

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')
    search_fields = ('name', 'user__username')
    list_filter = ('user',)

class ListeningHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'listened_at')
    search_fields = ('user__username', 'track__title', 'track__artist')
    list_filter = ('user',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(ListeningHistory, ListeningHistoryAdmin)