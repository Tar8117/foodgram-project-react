from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from users.serializers import UserSerializer

from .fields import Base64ImageField
from .models import (AddIngredientInRec, FavoriteRecipe, Ingredient, Recipe,
                     Tag, User)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class IngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = AddIngredientInRec
        fields = ('id', 'name', 'amount', 'measurement_unit')
        read_only_fields = ('amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientReadSerializer(source='amounts', many=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'text',
            'image',
            'ingredients',
            'tags',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.is_favorited.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.is_in_shopping_cart.filter(user=user).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'text',
            'image',
            'ingredients',
            'tags',
            'cooking_time',
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients_data:
            amount = ingredient['amount']
            id = ingredient['id']
            AddIngredientInRec.objects.create(
                ingredient=get_object_or_404(Ingredient, id=id),
                recipe=recipe, amount=amount
            )
        for tag in tags_data:
            recipe.tags.add(tag)
        return recipe

    def validate(self, data):
        ingredients_data = data['ingredients']
        ingredients_set = set()
        for ingredient in ingredients_data:
            if ingredient['amount'] <= 0:
                raise serializers.ValidationError(
                    'Вес ингредиента должен быть больше 0'
                )
            if ingredient['id'] in ingredients_set:
                raise serializers.ValidationError(
                    'Ингредиент в рецепте не должен повторяться.'
                )
            ingredients_set.add(ingredient['id'])
        return data

    def validate_cooking_time(self, data):
        cooking_time = self.initial_data.get('cooking_time')
        if not int(cooking_time) > 0:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше 0'
            )
        return data

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        AddIngredientInRec.objects.filter(recipe=instance).delete()
        for ingredient in ingredients_data:
            amount = ingredient['amount']
            id = ingredient['id']
            AddIngredientInRec.objects.create(
                ingredient=get_object_or_404(Ingredient, id=id),
                recipe=instance, amount=amount
            )
        instance.save()
        instance.tags.set(tags_data)
        return instance

    def to_representation(self, instance):
        data = RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = FavoriteRecipe
        fields = (
            'user',
            'recipe'
        )

    def validate(self, obj):
        user = self.context['request'].user
        recipe = obj['recipe']

        if (self.context.get('request').method == 'GET'
                and user.is_favorited.filter(recipe=recipe).exists()):
            raise serializers.ValidationError(
                'Этот рецепт уже есть в избранном')

        if (self.context.get('request').method == 'DELETE'
                and not user.is_favorited.filter(recipe=recipe).exists()):
            raise serializers.ValidationError(
                'Этого рецепта не было в вашем избранном')

        return obj


class ShoppingCartSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = FavoriteRecipe
        fields = (
            'user',
            'recipe'
        )

    def validate(self, obj):
        user = self.context['request'].user
        recipe = obj['recipe']

        if (self.context.get('request').method == 'GET'
                and user.is_in_shopping_cart.filter(recipe=recipe).exists()):
            raise serializers.ValidationError(
                'Этот рецепт уже есть в списке покупок')

        if (self.context.get('request').method == 'DELETE' and
                not user.is_in_shopping_cart.filter(recipe=recipe).exists()):
            raise serializers.ValidationError(
                'Этого рецепта не было в вашем списке покупок')

        return obj
