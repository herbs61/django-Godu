# Generated by Django 5.2 on 2025-05-07 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_member_email_verified_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                default="profile_pictures/default.png",
                upload_to="profile_pictures/",
            ),
        ),
    ]
