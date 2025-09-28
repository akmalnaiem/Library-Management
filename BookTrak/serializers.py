from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import UserProfile
from .models import Book



# Serializer for User's Registration--
class UserRegistrationSerializer(serializers.ModelSerializer):
    #Adding confirm_password field (not part of User model)
    confirm_password = serializers.CharField(write_only = True)
    user_type = serializers.ChoiceField(choices=UserProfile.USER_TYPES, default='customer')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'user_type']
        extra_kwargs = {
            'password' : {'write_only' : True},
            'email': {'required': True} 
        }
    
    def validate_email(self, value):
        #Validating email is unique
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email is already exist")
        return value
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password":"Password do not match"})
        return data
    
    def create(self, validated_data):
        user_type = validated_data.pop('user_type', 'customer')
        """Creating a new user"""
        validated_data.pop('confirm_password')          # Removing confirm_password field, not require for user creation

        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )

        UserProfile.objects.create(user=user, user_type=user_type)
        return user
    

# Serializer for User's Login--
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                    return data
                raise serializers.ValidationError("User account is disabled")
            raise serializers.ValidationError("Unable to login with this credentials")
        raise serializers.ValidationError("Please provide both the credentials")
    


# Serializer for Adding/Delete Books--
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'price', 'cover_image_url']
        read_only_fields = ['id']          # this is auto-generated


# Serializer for Book Report--
class BookReportSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(source = 'id')           # provide id source to it
    title = serializers.CharField()
    author = serializers.CharField()
    total_issues = serializers.IntegerField(source = 'times_issued')



# Serializer for Browse Books--
class BrowseBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'cover_image_url', 'times_issued']



# Serializer for saving Book--
class SaveLaterSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

    def validate_book_id(self, value):
        if not Book.objects.filter(id=value).exists():
            raise serializers.ValidationError("Book does not exist.")
        return value



# Serializer for Cart system--
class BookCartSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

    def validate_book_id(self, value):
        if not Book.objects.filter(id=value).exists():
            raise serializers.ValidationError("Book does not exist.")
        return value



# Checkout serializer--
class CheckoutSerializer(serializers.Serializer):
    books_to_issue = serializers.ListField(
        child = serializers.IntegerField(),
        help_text = "List of book IDs from the cart that user want to issue."
    )

    def validate_books_to_issue(self, value):
        if not value:
            raise serializers.ValidationError("Please select at least one book to issue.")
        return value
    



