# Generated by Django 4.0.5 on 2022-06-07 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('type', models.CharField(default='album', max_length=55)),
                ('total_tracks', models.BigIntegerField(default=0)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('release_date_precision', models.CharField(blank=True, max_length=150, null=True)),
                ('uri', models.CharField(blank=True, max_length=150, null=True)),
                ('available_markets', models.JSONField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.CharField(max_length=100)),
                ('short_bio', models.CharField(blank=True, max_length=255, null=True)),
                ('popularity', models.BigIntegerField(default=0)),
                ('external_urls', models.CharField(blank=True, max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_name', models.CharField(max_length=200)),
                ('url', models.FileField(upload_to='track/')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('album_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albums.album')),
            ],
        ),
        migrations.CreateModel(
            name='ArtistsImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.FileField(upload_to='artist_image/')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('artist_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albums.artist')),
            ],
        ),
        migrations.CreateModel(
            name='AlbumsImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.FileField(upload_to='albums_image/')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('album_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albums.album')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ManyToManyField(to='albums.artist'),
        ),
    ]
