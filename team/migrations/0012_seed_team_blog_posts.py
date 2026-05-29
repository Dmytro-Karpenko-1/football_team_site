from django.db import migrations
from django.utils import timezone


POSTS = [
    (
        "Як проходять тренування команди",
        "На тренуваннях діти багато працюють з м'ячем, виконують вправи на координацію, швидкість і прості ігрові рішення. Головне завдання — допомогти дитині рухатися впевнено та отримувати задоволення від футболу.",
    ),
    (
        "Перші матчі та командний досвід",
        "Матчі на вихідних допомагають дітям застосовувати навички в реальній грі. Для юних футболістів це досвід взаємодії, підтримки партнерів і перших футбольних емоцій.",
    ),
    (
        "Чому важлива регулярність тренувань",
        "Три тренування на тиждень формують звичку до руху, дисципліну та поступовий прогрес. У дитячому футболі стабільність часто важливіша за складні тактичні завдання.",
    ),
    (
        "Командна гра для дітей 2018 р.н.",
        "У цьому віці діти вчаться бачити партнерів, домовлятися на полі та підтримувати одне одного. Командність розвивається через прості вправи, міні-ігри та спільні матчі.",
    ),
    (
        "Роль батьків у дитячому футболі",
        "Підтримка батьків дуже важлива: дитині легше розвиватися, коли поруч є спокійна мотивація, увага та позитивне ставлення до тренувань і матчів.",
    ),
    (
        "Що взяти на пробне тренування",
        "Для першого заняття достатньо зручної спортивної форми, взуття для тренування та води. На пробному тренуванні дитина знайомиться з командою, тренером і форматом занять.",
    ),
]


def seed_blog_posts(apps, schema_editor):
    Team = apps.get_model('team', 'Team')
    BlogPost = apps.get_model('team', 'BlogPost')

    team, _ = Team.objects.get_or_create(
        name="ФК Зазим'є",
        defaults={
            'description': "Дитяча футбольна команда з села Зазим'є.",
            'founded_year': 2023,
            'city': "Зазим'є",
        },
    )

    BlogPost.objects.filter(title__icontains='Tackle').update(
        title=POSTS[0][0],
        content=POSTS[0][1],
        author="ФК Зазим'є",
        is_published=True,
    )
    BlogPost.objects.filter(content__icontains='ibis-gear').update(
        title=POSTS[0][0],
        content=POSTS[0][1],
        author="ФК Зазим'є",
        is_published=True,
    )

    for index, (title, content) in enumerate(POSTS):
        BlogPost.objects.get_or_create(
            title=title,
            defaults={
                'team': team,
                'content': content,
                'author': "ФК Зазим'є",
                'is_published': True,
                'created_at': timezone.now() - timezone.timedelta(days=index),
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0011_simplify_joinapplication'),
    ]

    operations = [
        migrations.RunPython(seed_blog_posts, migrations.RunPython.noop),
    ]
