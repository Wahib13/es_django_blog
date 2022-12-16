# Generated by Django 4.0.8 on 2022-12-16 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jewels', '0001_initial'),
        ('blogs', '0008_author_alter_category_slug_alter_post_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jewels.author'),
        ),
    ]
