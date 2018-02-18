from django.shortcuts import render,redirect
from django.contrib import messages
from airtable import Airtable
import os #to interact with environment variables(to be discussed later){safe way of storing api keys}

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
                            'Movies',
                            api_key=os.environ.get('AIRTABLE_API_KEY'))
# Create your views here.
def home_page(request):
#     print(str(request.GET.get('query','')))
    user_query = str(request.GET.get('query',''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "',LOWER({Name}))")
    stuff_for_frontend = {'search_result' : search_result}
    return render(request,'movies/movies_stuff.html',stuff_for_frontend)

def create(request):
    if request.method == 'POST':
        data = {
            'Name' : request.POST.get('name'),
            'Pictures' : [{'url':request.POST.get('url') or 'http://vollrath.com/ClientCss/images/VollrathImages/No_Image_Available.jpg'}],
            'Rating' : int(request.POST.get('rating')),
            'Notes' : request.POST.get('notes')
        }
        try:
            response = AT.insert(data)
            #notify on create
            messages.success(request,"New Movie Added: {}".format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request,"Got an error when trying to create a new movie: {}".format(e))
    return redirect('/')

def edit(request, movie_id):
    if request.method == 'POST':
        data = {
            'Name' : request.POST.get('name'),
            'Pictures' : [{'url':request.POST.get('url')}],
            'Rating' : int(request.POST.get('rating')),
            'Notes' : request.POST.get('notes')
        }
        try:
            response = AT.update(movie_id,data)
            messages.success(request,"Updated Movie: {}".format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request,"Got an error while trying to update the movie: {}".format(e))
    return redirect('/')

def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id).get('fields').get('Name')
        AT.delete(movie_id)
        messages.warning(request, "Deleted Movie: {}".format(movie_name))
    except Exception as e:
        messages.warning(request, "Got an error while tring to delete a movie: {}".format(e))

    return redirect('/')




