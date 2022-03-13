# Generated by Django 3.2.12 on 2022-03-12 06:56

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='infosite',
            name='favicon',
            field=filebrowser.fields.FileBrowseField(blank=True, max_length=200, verbose_name='Favicon'),
        ),
        migrations.AlterField(
            model_name='infosite',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]