# Generated by Django 4.2.20 on 2025-05-04 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authz', '0003_alter_organizationalunit_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpermission',
            name='permission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='authz.permissiontype'),
        ),
    ]
