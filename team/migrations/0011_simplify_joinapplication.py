from django.db import migrations, models


def copy_join_application_data(apps, schema_editor):
    JoinApplication = apps.get_model('team', 'JoinApplication')
    for application in JoinApplication.objects.all():
        application.child_name = application.first_name
        application.parent_phone = application.phone
        application.age = '6'
        application.save(update_fields=['child_name', 'parent_phone', 'age'])


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0010_homeherovisual'),
    ]

    operations = [
        migrations.AddField(
            model_name='joinapplication',
            name='age',
            field=models.CharField(
                choices=[('5', '5 років'), ('6', '6 років'), ('7', '7 років'), ('8', '8 років')],
                default='6',
                max_length=2,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='joinapplication',
            name='child_name',
            field=models.CharField(default='', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='joinapplication',
            name='parent_phone',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.RunPython(copy_join_application_data, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='joinapplication',
            name='email',
        ),
        migrations.RemoveField(
            model_name='joinapplication',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='joinapplication',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='joinapplication',
            name='message',
        ),
        migrations.RemoveField(
            model_name='joinapplication',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='joinapplication',
            name='position',
        ),
    ]
