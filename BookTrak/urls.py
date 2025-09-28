from django.urls import path
from .views import *


urlpatterns = [
    # API endpoint for handling Registration/Login--
    path("api/registration/", UserRegistrationView.as_view(), name="userRegister"),
    path("api/login/", UserLoginView.as_view(), name="userLogin"),

    # API endpoint for different user type (Librarian and Customer)--
    path("api/librarian/", LibrarianView.as_view(), name="librarianPanel"),
    path("api/customer/", CustomerView.as_view(), name="customerPanel"),

    # API endpoint for Librarian to add book--
    path("api/librarian/add-books/", BookAddCreate.as_view(), name="add_books"),
    # API endpoint for Librarian to delete the book--
    path("api/librarian/delete-books/<int:id>/", BookDestroyView.as_view(), name="delete_books"),

    # API endpoint for Librarian to see the book-report--
    path("api/librarian/report/", BookReport.as_view(), name="bookReport"),

    # API endpoint for Customer to browse book--
    path("api/customer/browse-book/", BrowseBook.as_view(), name="browseBook"),

    # API endpoint for customer to save book for save later--
    path("api/customer/save-book/", SaveLater.as_view(), name="saveLater"),

    # API endpoint for customer to add book to cart --
    path("api/customer/add-to-cart/", AddToCart.as_view(), name="add_to_cart"),
    # API endpoint for customer to remove book from cart--
    path("api/customer/remove-from-cart/", RemoveFromCart.as_view(), name="remove_from_cart"),

    # API endpoint for customer to checkout--
    path("api/customer/checkout/", Checkout.as_view(), name="checkout"),

    # # API endpoint to see all the saved books--
    # path("api/saved-books/", SavedBooks.as_view(), name="saved-books")
]