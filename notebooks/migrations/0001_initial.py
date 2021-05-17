# Generated by Django 3.0.10 on 2020-09-19 15:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sheet',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this sheet should be treated as active. Unselect this instead of deleting sheet.', verbose_name='active status')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customersheets', to=settings.AUTH_USER_MODEL)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchantsheets', to=settings.AUTH_USER_MODEL)),
                ('profiles', models.ManyToManyField(blank=True, related_name='sheetprofiles', to='accounts.Profile')),
            ],
            options={
                'verbose_name': 'sheet',
                'verbose_name_plural': 'sheets',
                'unique_together': {('merchant', 'customer')},
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('note', models.CharField(blank=True, max_length=255, verbose_name='note')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='value')),
                ('operation', models.CharField(choices=[('credit', 'credit'), ('debt', 'debt')], db_index=True, max_length=30, verbose_name='operation')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this record should be treated as active. Unselect this instead of deleting record.', verbose_name='active status')),
                ('attendant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendantrecords', to='accounts.Profile')),
                ('sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sheetrecords', to='notebooks.Sheet')),
                ('signatary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signataryrecords', to='accounts.Profile')),
            ],
            options={
                'verbose_name': 'record',
                'verbose_name_plural': 'records',
            },
        ),
    ]