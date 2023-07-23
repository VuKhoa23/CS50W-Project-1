from django.shortcuts import render
from . import util
import markdown2
from django import forms
from django.http import HttpResponseRedirect
import random as rd

class SearchForm(forms.Form):
    searchValue = forms.CharField(label="Search",widget = forms.TextInput(attrs={
            'placeholder': 'Search Encyclopedia'}), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchForm": SearchForm()
    })

def get_entry(request, title):
    return render(request, "encyclopedia/show-wiki.html", {
        "entries": util.list_entries(),
        "wiki_entry": markdown2.markdown(util.get_entry(title)),
        "searchForm": SearchForm(),
        "title": title
    })

def get_searched_entry(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            searchValue = form.cleaned_data["searchValue"]
            entries = util.list_entries()
            for entry in entries:
                if entry.lower() == searchValue.lower():
                    return render(request, "encyclopedia/show-wiki.html", {
                    "entries": util.list_entries(),
                    "wiki_entry": markdown2.markdown(util.get_entry(entry)),
                    "searchForm": SearchForm()})
            cnt = 0
            sub_entries = []
            for entry in entries:
                if searchValue.lower() in entry.lower():
                    sub_entries.append(entry)
                    cnt += 1
            if cnt > 0:
                return render(request, "encyclopedia/search-result.html", {
                    "entries": sub_entries,
                    "searchForm": SearchForm()})
            else:
                return HttpResponseRedirect("error/not-found")
        
def random(request):
    entries = util.list_entries()
    randomed = rd.choice(entries)
    return HttpResponseRedirect(f"{randomed}")

def edit(request):
    if request.method == "POST":
        title = request.POST.get('mytitle', False)  
    return render(request, "encyclopedia/edit-wiki.html", {
            "entries": util.list_entries(),
            "wiki_entry": util.get_entry(title),
            "searchForm": SearchForm(),
            "title": title})

def edit_save(request):
    if request.method == "POST":
        content = request.POST.get('edit_content', False)
        title = request.POST.get('title', False)
        util.save_entry(title, content)
    return HttpResponseRedirect(f"{title}")
            
def create(request):
     return render(request, "encyclopedia/create-form.html", {
        "searchForm": SearchForm()
    })

def error(request, error):
    return render(request, "encyclopedia/error.html", {
        "error": error,
        "entries": util.list_entries(),
        "searchForm": SearchForm()

    })

def create_save(request):
    entries = util.list_entries()
    if request.method == "POST":
        content = request.POST.get('new_page_content', False)
        title = request.POST.get('title', False)
        for entry in entries:
            if entry.lower() == title.lower():
                return HttpResponseRedirect("error/new_page_err")
        util.save_entry(title, content)
    return HttpResponseRedirect(f"{title}")
