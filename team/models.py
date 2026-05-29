from datetime import date

from django.db import models


class HeroBackground(models.Model):
    """Hero background image for a specific site page."""
    PAGE_CHOICES = [
        ('home', 'Головна'),
        ('about', 'Про нас'),
        ('matches', 'Матчі'),
        ('standings', 'Таблиця'),
        ('blog', 'Блог'),
        ('join', 'Приєднатися'),
        ('sponsors', 'Спонсори'),
    ]

    page = models.CharField(max_length=30, choices=PAGE_CHOICES, unique=True)
    image = models.ImageField(upload_to='hero_backgrounds/', blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_page_display()

    class Meta:
        verbose_name = 'Фон верхнього блоку'
        verbose_name_plural = 'Фони верхніх блоків'
        ordering = ['page']


class HomeHeroVisual(models.Model):
    """Right-side visual image on the home page hero."""
    title = models.CharField(max_length=100, default='Головний візуал')
    image = models.ImageField(upload_to='home_hero/', blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Головний візуал'
        verbose_name_plural = 'Головний візуал'


class HomeGalleryImage(models.Model):
    """Image displayed in the home page team life gallery."""
    title = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to='home_gallery/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or f'Фото #{self.order}'

    class Meta:
        verbose_name = 'Фото життя команди'
        verbose_name_plural = 'Фото життя команди'
        ordering = ['order', 'id']


class Team(models.Model):
    """Team model"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    founded_year = models.IntegerField()
    logo = models.ImageField(upload_to='team/', blank=True)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команди'


class Player(models.Model):
    """Player model"""
    POSITIONS = [
        ('GK', 'Воротар'),
        ('DEF', 'Захисник'),
        ('MID', 'Півзахисник'),
        ('FWD', 'Нападник'),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=3, choices=POSITIONS)
    number = models.IntegerField()
    photo = models.ImageField(upload_to='players/', blank=True)
    birth_date = models.DateField()
    nationality = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    class Meta:
        verbose_name = 'Гравець'
        verbose_name_plural = 'Гравці'


class Coach(models.Model):
    """Coach model"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='coaches')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)  # e.g., Head Coach, Assistant
    photo = models.ImageField(upload_to='coaches/', blank=True)
    bio = models.TextField()
    experience = models.IntegerField()  # years of experience
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренери'


class Match(models.Model):
    """Match model"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches')
    opponent = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='opponent_matches')
    match_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    team_goals = models.IntegerField(null=True, blank=True)
    opponent_goals = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[('upcoming', 'Майбутній'), ('played', 'Зіграний')],
        default='upcoming'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.team} vs {self.opponent}"

    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчі'


class Standing(models.Model):
    """League Standing model"""
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='standing')
    display_name = models.CharField(max_length=100, blank=True)
    position = models.IntegerField()
    played = models.IntegerField(default=0)
    won = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against

    def __str__(self):
        return f"{self.position}. {self.display_name or self.team.name}"

    class Meta:
        verbose_name = 'Таблиця'
        verbose_name_plural = 'Таблиці'


class BlogPost(models.Model):
    """Blog Post model"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blog/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост блогу'
        verbose_name_plural = 'Пости блогу'
        ordering = ['-created_at']


class Sponsor(models.Model):
    """Sponsor model"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='sponsors')
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='team/', blank=True)
    website = models.URLField(blank=True)
    level = models.CharField(
        max_length=20,
        choices=[('gold', 'Золотий'), ('silver', 'Срібний'), ('bronze', 'Бронзовий')],
        default='bronze'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Спонсор'
        verbose_name_plural = 'Спонсори'


class JoinApplication(models.Model):
    """Application submitted by a parent for a trial training."""
    AGE_CHOICES = [
        ('5', '5 років'),
        ('6', '6 років'),
        ('7', '7 років'),
        ('8', '8 років'),
    ]

    child_name = models.CharField(max_length=120)
    parent_phone = models.CharField(max_length=20)
    age = models.CharField(max_length=2, choices=AGE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.child_name} - {self.parent_phone}"

    class Meta:
        verbose_name = 'Заявка до команди'
        verbose_name_plural = 'Заявки до команди'
        ordering = ['-created_at']
