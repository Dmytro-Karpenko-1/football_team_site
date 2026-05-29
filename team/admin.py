from django.contrib import admin
from .models import HeroBackground, HomeHeroVisual, Team, Player, Coach, Match, Standing, BlogPost, Sponsor, JoinApplication


@admin.register(HeroBackground)
class HeroBackgroundAdmin(admin.ModelAdmin):
    list_display = ('page', 'image', 'is_active', 'updated_at')
    list_filter = ('page', 'is_active')
    readonly_fields = ('updated_at',)


@admin.register(HomeHeroVisual)
class HomeHeroVisualAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    readonly_fields = ('updated_at',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'founded_year')
    search_fields = ('name', 'city')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'team', 'position', 'number')
    list_filter = ('team', 'position')
    search_fields = ('first_name', 'last_name', 'team__name')


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'team', 'position')
    list_filter = ('team',)
    search_fields = ('first_name', 'last_name', 'team__name')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('team', 'opponent', 'match_date', 'status')
    list_filter = ('team', 'status', 'match_date')
    search_fields = ('opponent__name', 'team__name')


@admin.register(Standing)
class StandingAdmin(admin.ModelAdmin):
    list_display = ('position', 'team', 'points', 'played', 'goal_difference')
    list_filter = ('position',)
    search_fields = ('team__name',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'team', 'author', 'is_published', 'created_at')
    list_filter = ('team', 'is_published', 'created_at')
    search_fields = ('title', 'author', 'team__name')
    date_hierarchy = 'created_at'


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'level')
    list_filter = ('team', 'level')
    search_fields = ('name', 'team__name')


@admin.register(JoinApplication)
class JoinApplicationAdmin(admin.ModelAdmin):
    list_display = ('child_name', 'parent_phone', 'age', 'is_processed', 'created_at')
    list_filter = ('age', 'is_processed', 'created_at')
    search_fields = ('child_name', 'parent_phone')
    readonly_fields = ('created_at',)
