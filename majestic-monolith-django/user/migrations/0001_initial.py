# Generated by Django 3.2.4 on 2022-03-07 14:04

import core.fields
import core.utils
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=128, null=True, region=None, unique=True)),
                ('phonenumber_meta', models.CharField(blank=True, db_index=True, help_text='Flag for banned user', max_length=32)),
                ('username', models.CharField(blank=True, default='', error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=15, unique=True, verbose_name='username')),
                ('type', models.CharField(choices=[('STAFF', 'Staff'), ('DRIVER', 'Driver')], default='STAFF', max_length=10, verbose_name='Type')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('banned', models.BooleanField(db_index=True, default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('locale', models.CharField(default='en', max_length=10)),
                ('date_unregistered', models.DateTimeField(default=None, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'auth_user',
                'ordering': ['-id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfileStaff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(blank=True, default='', max_length=32)),
                ('image', core.fields.ThumbnailerImageField(upload_to=core.utils.UserPathAndRename('images/user/staff/'))),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile_staff',
            },
        ),
        migrations.CreateModel(
            name='UserProfileDriver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(blank=True, default='', max_length=32)),
                ('dob', models.DateField(blank=True, default=None, null=True)),
                ('image', core.fields.ThumbnailerImageField(upload_to=core.utils.UserPathAndRename('images/user/driver/'))),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile_driver',
            },
        ),
        migrations.CreateModel(
            name='UserDriver',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user.customuser',),
        ),
        migrations.CreateModel(
            name='UserStaff',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user.customuser',),
        ),
    ]
