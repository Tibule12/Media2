# Generated migration file to add non-nullable 'actor' field to Notification model with a default value

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

def default_actor(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    return User.objects.first().pk if User.objects.exists() else 1

class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='actor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='actions', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
