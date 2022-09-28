from django.contrib import admin, messages
from .models import Movie, Director, Actor, DressingRoom
from django.db.models import QuerySet

# Register your models here.

admin.site.register(Director)
admin.site.register(Actor)
# admin.site.register(DressingRoom)


# class for own filter
class RatingFilter(admin.SimpleListFilter):
    title = 'Rating filter'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [
            ('<40', 'Low rating'),
            ('from 40 to 59', 'Average rating'),
            ('from 60 to 79', 'High rating'),
            ('>=80', 'Highest rating')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<40':
            return queryset.filter(rating__lt=40)
        if self.value() == 'from 40 to 59':
            return queryset.filter(rating__lt=60).filter(rating__gt=39)
        if self.value() == 'from 60 to 79':
            return queryset.filter(rating__lt=80).filter(rating__gt=59)
        if self.value() == '>=80':
            return queryset.filter(rating__gt=79)
        return queryset


# Create Class for additional DB view setting on Django Admin Page
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # raring_status taken fom method below - additional field in response
    list_display = ['name', 'rating', 'director', 'budget', 'rating_status']
    list_editable = ['rating', 'director', 'budget']
    ordering = ['-rating', 'name']  # sorting by ...
    list_per_page = 3  # Quantity of movies in list per one page
    actions = ['set_dollars', 'set_euro']  # register action for django admin panel - set currency to USD and EURO
    # search_fields = ['name', 'rating'] # add search field to django admin panel - searching by name or raring (or - due to different variable type)
    search_fields = ['name__startswith', 'rating']  # add search field to django admin panel - searching by name start with... or raring (or - due to different variable type)
    # search_fields = ['name__istartswith', 'rating'] # add search field to django admin panel - searching by name start with... or raring (or - due to different variable type) istartswith - not
    # sensible to letter register
    list_filter = ['name', 'currency', RatingFilter]

    # add selection field (with arrows) to actors selection field
    filter_horizontal = ['actors']
    # filter_vertical = ['actors'] # similar to above, but vertical

    # create field which will be filled automatically during typing in field NAME
    prepopulated_fields = {'slug': ('name',)}

    # fields for adding movie in django admin panel
    # fields = ['name', 'rating']

    # hide following fields from adding movie at django admin panel
    # exclude = ['currency', 'budget', 'slug']

    # may use decorator instead of below method
    # admin.site.register(Movie, MovieAdmin)  # - registering our models and classes for Django Admin page

    # mov from method below is instance of class Movie (to see all attributes variable has to be annotated) !!!!!!
    # to make it sortable should be used decorator @admin.display()
    # description - name of the column in django-admin panel (without description it will be just method name)
    # ordering will work only if no ORDERING mentioned in MovieAdmin class
    @admin.display(ordering='rating', description='status')
    def rating_status(self, mov: Movie):
        if mov.rating <= 50:
            return 'poor movie'
        if mov.rating <= 75:
            return 'so-so movie'
        if mov.rating <= 85:
            return 'Good movie'
        return 'Top movie'

    # Add to django admin additional action in choice - set currency to USD
    @admin.action(description='Set currency to USD')
    def set_dollars(self, request, qs: QuerySet):
        qs.update(currency=Movie.USD)

    # Add to django admin additional action in choice - set currency to EURO
    @admin.action(description='Set currency to EURO')
    def set_euro(self, request, qs: QuerySet):
        count_update = qs.update(currency=Movie.EUR)
        self.message_user(
            request,
            f'updated {count_update} records',
            level=messages.WARNING
        )  # - show message how many records have been updated



@admin.register(DressingRoom)
class DressingRoomAdmin(admin.ModelAdmin):
    list_display = ['floor', 'room_number', 'actor']

