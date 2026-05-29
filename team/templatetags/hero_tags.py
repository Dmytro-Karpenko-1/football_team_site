import os

from django import template

from team.models import HeroBackground, HomeHeroVisual

register = template.Library()

DEFAULT_HERO_BACKGROUND = 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)'
HERO_IMAGE_OVERLAY = 'linear-gradient(135deg, rgba(5, 24, 55, 0.12), rgba(5, 24, 55, 0.04))'


def _optimized_image_url(image_field):
    root, _ = os.path.splitext(image_field.name)
    webp_name = f'{root}.webp'

    if image_field.storage.exists(webp_name):
        return image_field.storage.url(webp_name)

    return image_field.url


@register.simple_tag
def hero_background(page):
    hero = HeroBackground.objects.filter(page=page, is_active=True).first()
    if not hero or not hero.image:
        return DEFAULT_HERO_BACKGROUND

    version = int(hero.updated_at.timestamp()) if hero.updated_at else 0
    return f"{HERO_IMAGE_OVERLAY}, url('{_optimized_image_url(hero.image)}?v={version}') center/cover no-repeat"


@register.simple_tag
def home_hero_visual_url():
    visual = HomeHeroVisual.objects.filter(is_active=True).exclude(image='').order_by('-updated_at').first()
    if not visual or not visual.image:
        return ''

    version = int(visual.updated_at.timestamp()) if visual.updated_at else 0
    return f'{_optimized_image_url(visual.image)}?v={version}'
