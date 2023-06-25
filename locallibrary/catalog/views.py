# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
import datetime
from .forms import RenewBookForm
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView

def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Libros disponibles (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # El 'all()' esta implícito por defecto.
    num_genre=Genre.objects.count()
    num_books_with_Oriente=Book.objects.filter(title__icontains='Oriente').count()
    # Renderiza la plantilla HTML index.html con los datos en la variable contexto

    # Numero de visitas a esta view, como está contado en la variable de sesión.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors, 'num_genre':num_genre, 'num_books_with_Oriente': num_books_with_Oriente, 'num_visits':num_visits},
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksByLibrarianListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = (('catalog.can_mark_returned'),)

    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})    

class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    
    permission_required = (('catalog.can_mark_returned'),)

    model = Author
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}

class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    
    permission_required = (('catalog.can_mark_returned'),)
    
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):

    permission_required = (('catalog.can_mark_returned'),)

    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    
    permission_required = (('catalog.can_mark_returned'),)

    model = Book
    fields = '__all__'

class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    
    permission_required = (('catalog.can_mark_returned'),)
    
    model = Book
    fields = ['title','author','summary','genre', 'isbn', 'language']

class BookDelete(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):

    permission_required = (('catalog.can_mark_returned'),)

    model = Book
    success_url = reverse_lazy('books')

def mi_vista(request):
    return HttpResponse("Hola, mundo!")