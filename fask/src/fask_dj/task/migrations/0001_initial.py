# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-19 10:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(help_text='The short description for that element', max_length=200, verbose_name='Description')),
                ('annotation', models.TextField(help_text='Here you can give more deep information', verbose_name='Annotation')),
                ('creation_date', models.DateField(auto_now_add=True, help_text='When the element was created', verbose_name='Creation Date')),
                ('edit_date', models.DateField(auto_now=True, help_text='When the element was modified last time', verbose_name='Edit Date')),
                ('creation_user', models.TextField(help_text='Who created the element', verbose_name='Creation User')),
                ('edit_user', models.TextField(help_text='Who modified the element last time', verbose_name='Edit User')),
                ('due_to', models.DateField(help_text='When task has to be completed', verbose_name='Due To')),
                ('completed_on', models.DateField(help_text='When task was completed', verbose_name='End Date')),
                ('assigned_to', models.ForeignKey(help_text='Who is executing the task', on_delete=django.db.models.deletion.CASCADE, related_name='task_assignee', to=settings.AUTH_USER_MODEL, verbose_name='Assigned To')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskPriority',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(help_text='The short description for that element', max_length=200, verbose_name='Description')),
                ('annotation', models.TextField(help_text='Here you can give more deep information', verbose_name='Annotation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskProgression',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(help_text='The short description for that element', max_length=200, verbose_name='Description')),
                ('annotation', models.TextField(help_text='Here you can give more deep information', verbose_name='Annotation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.ForeignKey(help_text='How the task is urgent', on_delete=django.db.models.deletion.CASCADE, related_name='task_priority', to='task.TaskPriority', verbose_name='Priority'),
        ),
        migrations.AddField(
            model_name='task',
            name='progression',
            field=models.ForeignKey(help_text='What is the progression state of the task', on_delete=django.db.models.deletion.CASCADE, related_name='task_progression', to='task.TaskProgression', verbose_name='Proression'),
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(help_text='The project that is the task owner', on_delete=django.db.models.deletion.CASCADE, related_name='task_project_owner', to='project.Project', verbose_name='Project'),
        ),
    ]
