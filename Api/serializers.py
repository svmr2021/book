from django.db import transaction
from rest_framework import serializers
from library.models import Person, Book, Comment, Like, Category, Book_Category
from django.contrib.auth.models import User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'publisher']

    def to_representation(self, instance):
        data = super(CommentSerializer, self).to_representation(instance)
        publisher = data['publisher']
        obj = User.objects.get(id=publisher)
        data['publisher'] = obj.username
        return data


class CommentCreateSerializer(serializers.ModelSerializer):
    publisher = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['text', 'book_name', 'publisher']


class CommentUpdateSerializer(serializers.ModelSerializer):
    publisher = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['text', 'publisher']


class LikeCreateSerializer(serializers.ModelSerializer):
    liked = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ['book_name', 'liked']


class CategorySerializer(serializers.ModelSerializer):
    publisher = serializers.ReadOnlyField(source='publisher.username')
    book_name = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'publisher', 'book_name']


class UserSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'categories']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

            return user


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class PersonCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    type_of_user = serializers.HiddenField(default="Reader")
    age = serializers.IntegerField(min_value=0)

    class Meta:
        model = Person
        fields = '__all__'


class PersonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['firstname', 'lastname', 'age', 'email']


class BookSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(source='comments', many=True)
    liked = LikeCreateSerializer(source='likes',many=True)
    #categories = CategorySerializer(source='category_name')

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'updated_at', 'date_published', 'publisher', 'comment', 'categories', 'liked','description','image')

    def to_representation(self, instance):
        data = super(BookSerializer, self).to_representation(instance)
        category = data['categories']
        publisher = data['publisher']
        likes = data['liked']
        list = []
        for i in category:
            object = Category.objects.get(id=i)
            list.append(object.name)
        data['categories'] = list
        pub = User.objects.get(id=publisher)
        data['publisher'] = pub.username
        data['liked'] = len(likes)
        return data


class BookCreateSerializer(serializers.ModelSerializer):
    publisher = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'date_published','description','image','publisher', 'category']

    def create(self, validated_data):

        category = validated_data.pop('category')
        print(category)
        book = Book.objects.create(**validated_data)
        for i in range(len(category)):
            categ = Book_Category(book_name=book, category_name=category[i])
            categ.save()
        return book


class BookUpdateSerializer(serializers.ModelSerializer):
    publisher = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_at = serializers.HiddenField(default=serializers.DateTimeField())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),many=True,write_only=True)

    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher','date_published', 'updated_at','category','categories']
        read_only_fields = ('categories',)

    def to_representation(self, instance):
        data = super(BookUpdateSerializer, self).to_representation(instance)
        category = data['categories']
        list = []
        for i in category:
            object = Category.objects.get(id=i)
            list.append(object.name)
        data['categories'] = list
        return data

    def update(self, instance, validated_data):
        print(validated_data)
        category = validated_data.pop('category')
        title = validated_data['title']
        instance.title = validated_data.get('title',instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.date_published = validated_data.get('date_published', instance.date_published)
        instance.save()
        book = Book.objects.get(title=title)
        for i in range(len(category)):
            categ = Book_Category(book_name=book, category_name=category[i])
            categ.save()

        return instance