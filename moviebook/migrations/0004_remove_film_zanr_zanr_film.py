# Generated by Django 4.2 on 2023-04-16 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moviebook', '0003_remove_zanr_film_film_zanr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='film',
            name='zanr',
        ),
        migrations.AddField(
            model_name='zanr',
            name='film',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='moviebook.film'),
        ),
    ]