import random
from django.shortcuts import render, redirect
from django import forms
import markdown2 
from markdown2 import Markdown
from . import util

markdowner=Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        contents = util.get_entry(title)
        contents = markdown2.markdown(contents)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": contents
        })
    else:
        return render(request, "encyclopedia/error.html", {
                "errorMessage": "This page does not exist!"
            })

def randomEntry(request):
    if request.method == "GET":
        entries = util.list_entries()
        r = random.randint(0, len(entries) - 1)
        page = entries[r]
        return redirect(entry, title = page)

def search(request):
    if request.method == 'POST':
        entries = util.list_entries()
        look = request.POST.get('q')
        if look in entries:
            contents = util.get_entry(look)
            contents = markdown2.markdown(contents)
            return render(request, "encyclopedia/entry.html", {
                "title": look,
                "content": contents
            })
        results = []
        for entry in entries:
            lookt = look.lower()
            temp = entry.lower()
            if temp.find(lookt) != -1:
                results.append(entry)
        if len(results) == 0:
            return render(request, "encyclopedia/error.html", {
                "errorMessage": "No results for '{}'".format(look)
            })
        return render(request, "encyclopedia/search.html", {
                "entries": results
            })

def edit(request, title):
    if request.method == "GET":
        contents = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            'title': title,
            'content': contents
        })
    if request.method == "POST":
        contents = request.POST.get('contentEdit')
        util.save_entry(title, contents)
        return redirect(entry, title=title)

def create(request):
    if request.method == "POST":
        entries = util.list_entries()
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title in entries:
            return render(request, "encyclopedia/error.html", {
                "errorMessage": "This page already exists!"
            })
        else:
            util.save_entry(title, content)
            return redirect(entry, title=title)
    else:
        return render(request, "encyclopedia/create.html")