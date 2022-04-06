# Generated by Django 4.0.3 on 2022-04-05 23:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_in_shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.AddIngredientInRec', to='recipes.ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.tag', verbose_name='Теги'),
        ),
        migrations.AddField(
            model_name='follow',
            name='author',
            field=models.ForeignKey(help_text='На кого подписываются', on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(help_text='Кто подписывается', on_delete=django.db.models.deletion.CASCADE, related_name='subscribed_on', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='favoriterecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_favorited', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='favoriterecipe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_favorited', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='addingredientinrec',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amounts', to='recipes.ingredient', verbose_name='Ингридиент'),
        ),
        migrations.AddField(
            model_name='addingredientinrec',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amounts', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddConstraint(
            model_name='shoppinglist',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='cart_user_recept_unique'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='subscribe'),
        ),
        migrations.AddConstraint(
            model_name='favoriterecipe',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='user_recept_unique'),
        ),
        migrations.AddConstraint(
            model_name='addingredientinrec',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='recipe_ingredient_unique'),
        ),
    ]
