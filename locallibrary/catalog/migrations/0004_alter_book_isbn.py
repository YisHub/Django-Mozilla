# Generated by Django 4.2.1 on 2023-06-06 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_book_isbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(default='5145639767619', help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>*Si no se proporciona un ISBN, se generará uno aleatoriamente de 13 dígitos.*', max_length=13, unique=True, verbose_name='ISBN'),
        ),
    ]
