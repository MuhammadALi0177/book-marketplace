# Generated manually — password + auth_token + phone unique + telegram_id nullable

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0002_user_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="telegram_id",
            field=models.CharField(
                blank=True, db_index=True, max_length=64, null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(
                blank=True, db_index=True, max_length=32, null=True, unique=True
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="password_hash",
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="auth_token",
            field=models.CharField(
                blank=True, db_index=True, max_length=64, null=True, unique=True
            ),
        ),
    ]
