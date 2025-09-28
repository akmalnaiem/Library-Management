from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .serializers import UserRegistrationSerializer, UserLoginSerializer, BookSerializer, BookReportSerializer, BrowseBookSerializer, SaveLaterSerializer, BookCartSerializer, CheckoutSerializer
from rest_framework.views import APIView
from .permissions import IsLibrarian, IsCustomer
from rest_framework import generics
from .models import Book, UserProfile
from datetime import datetime, timedelta
from django.db import transaction
from django.http import JsonResponse
from collections import Counter


class LibrarianView(APIView):
    permission_classes = [IsLibrarian]

    def get(self, request):
        return Response({
            'message' : 'For Librarian only',
            'user_type' : request.user.userprofile.user_type
        })


class CustomerView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request):
        return Response({
            'message' : 'For Customers',
            'user_type' : request.user.userprofile.user_type
        })


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.save()        # Creates the user

            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'message' : 'User registered successfully',
                'token' : token.key,
                'user_id' : user.id,
                'username' : user.username
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            token, created = Token.objects.get_or_create(user=user)          # generating/getting existing token

            return Response({
                'message' : 'Login successful',
                'token' : token.key,
                'user_id' : user.id,
                'username' : user.username
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Librarian Actions--
# CBV for adding/listing the books by "Librarian" only--
class BookAddCreate(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarian]                                       # This allow only librarian to access(create/list) this CBV  



# CBV for retrieve/update/delete the books by "Librarian" only--
class BookDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarian]
    lookup_field = 'id'



# Making CBV for Book Report--
class BookReport(APIView):
    permission_classes = [IsLibrarian]

    def get(self,request):
        filter_type = request.GET.get('filter', 'most_issued')            # Taking filter the URL parameter (.../?filter = most_issued)

        books = Book.objects.all()

        # Applying sorting based on filter
        if filter_type == 'most_issued':
            books = books.order_by('-times_issued')                       # Descending order result
        elif filter_type == 'least_issued':
            books = books.order_by('times_issued')                        # Ascending order result
        elif filter_type == 'author':
            books = books.order_by('author', '-times_issued')             # A-Z order result

        # Serialize the data
        serializer = BookReportSerializer(books, many=True)

        return Response({
            'filter_applied' : filter_type,
            'total_books' : books.count(),
            'report' : serializer.data
        })
    

# Customer Actions--
# Making CBV for Browse Books--
class BrowseBook(APIView):
    permission_classes = [IsCustomer]

    def get(self, request):
        filter_type = request.GET.get('filter', 'most_issued')              # taking filter from URL parameter..

        books = Book.objects.all()

        # Applying sorting based on filter
        if filter_type == 'most_issued':
            books = books.order_by('-times_issued')
        elif filter_type == 'least_issued':
            books = books.order_by('times_issued')
        elif filter_type == 'author':
            books = books.order_by('author', 'title')

        # Serialize the books
        serializer = BrowseBookSerializer(books, many=True)

        return Response({
            'filter' : filter_type,
            'books_count' : books.count(),
            'books' : serializer.data
        })
    


# Making CBV for Save later--
class SaveLater(APIView):
    permission_classes = [IsCustomer]

    def post(self, request):
        serializer = SaveLaterSerializer(data = request.data)

        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']

            user_profile , created = UserProfile.objects.get_or_create(user = request.user)          # Get/Create user profile

            if book_id in user_profile.saved_books:                                                  # This check if book already saved (prevent duplicate)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user_profile.saved_books.append(book_id)
            user_profile.save()

            book = Book.objects.get(id=book_id)                                                       # get full book object

            return Response({
                'message' : "Book saved for later successfully",
                'saved_books_count' : len(user_profile.saved_books),
                'book_title' : book.title
            }, status=status.HTTP_202_ACCEPTED)              
            

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# CBV for Cart Add functionality--
class AddToCart(APIView):
    permission_classes = [IsCustomer]

    def post(self, request):
        serializer = BookCartSerializer(data = request.data)

        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']

            user_profile, created = UserProfile.objects.get_or_create(user = request.user)              # get user profile here

            user_profile.cart_items.append(book_id)                                                     # this appends book in cart item list and duplicates allow for quantity
            user_profile.save()

            book = Book.objects.get(id = book_id)

            return Response({
                'message' : 'Book added to cart successfully',
                'cart_items_count' : len(user_profile.cart_items),
                'book_title' : book.title
            }, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# CBV for Cart Remove functionality--
class RemoveFromCart(APIView):
    permission_classes = [IsCustomer]                                                                    # passing the permission 

    def delete(self, request):
        serializer = BookCartSerializer(data = request.data)

        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']
            user_profile = UserProfile.objects.get(user = request.user)

            if book_id in user_profile.cart_items:                                                        # checking the book is in cart or not 
                user_profile.cart_items.remove(book_id)                                                   # removing the book from cart
                user_profile.save()

                book = Book.objects.get(id = book_id)
                return Response({
                    'message' : 'Book removed from cart successfully',
                    'cart_items_count' : len(user_profile.cart_items),
                    'book_title' : book.title
                })
            else :
                return Response({'error':'Book not in cart'}, status=status.HTTP_400_BAD_REQUEST)         # if book not present than give error

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# CBV for checkout--
class Checkout(APIView):
    permission_classes = [IsCustomer]

    def post(self, request):
        serializer = CheckoutSerializer(data = request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        books_to_issue = serializer.validated_data['books_to_issue']
        user_profile = UserProfile.objects.get(user = request.user)

        missing_book = [book_id for book_id in books_to_issue if book_id not in user_profile.cart_items]              # Checking selected books in cart

        if missing_book:
            return Response({
                'error' : 'Some books are not in cart',
                'missing_books' : missing_book
            }, status=status.HTTP_400_BAD_REQUEST)
        
        issued_books = []
        total_amount = 0

        # Calculate date
        issue_date = datetime.now().date()
        return_date = issue_date + timedelta(days=14)

        with transaction.atomic():
            for book_id in books_to_issue:
                book = Book.objects.get(id=book_id)

                user_profile.cart_items.remove(book_id)                                                               # Remove book from cart

                book.times_issued +=1                                                                                 # update issue
                book.save()


                issued_books.append({
                    'title' : book.title,
                    'author' : book.author,
                    'price' : float(book.price)
                })
                total_amount += float(book.price)

            user_profile.save()

        bill_summary = {                                                                                              # Bill generation
            'total_books_issued' : len(issued_books),
            'total_amount' : round(total_amount, 2),
            'issue_date' : issue_date.strftime('%Y-%m-%d'),
            'return_date' : return_date.strftime('%Y-%m-%d'),
            'books_issued' : issued_books
        }

        return Response({
            'success' : True,
            'message' : 'Books issued successfully',
            'bill_summary' : bill_summary
        }, status=status.HTTP_200_OK)



# CBV to show saved books--
# class SavedBooks(generics.ListAPIView):
#     permission_classes = [IsCustomer]
#     serializer_class = BookSerializer

#     def get_queryset(self):
#         user_profile = UserProfile.objects.get(user = self.request.user)
#         return Book.objects.filter(id__in = user_profile.saved_books)



