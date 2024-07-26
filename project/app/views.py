from django.shortcuts import render,redirect
from .forms import CodeSnippetForm
import openai
from .models import CodeSnippet

# Create your views here.
def home(request):
    if request.method=='POST':
        form=CodeSnippetForm(request.POST)
        if form.is_valid():
            code_snippet=form.save(commit=False)
            code_snippet.documentation=generate_documentation(code_snippet.code)
            code_snippet.save()
            return redirect('detail',pk=code_snippet.pk)
    form=CodeSnippetForm()
    return render(request,"app\home.html",{'form':form})


def generate_documentation(code):
    response=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role":"system","content":"You are a helpful assistant"
            },
            {
                "role":"user","content":f"Generate documentation for the following code line by line code :\n\n{code}"
            }
        ],
        max_tokens=1000    )
    return response.choices[0].message['content'].strip()


def detail(request,pk):
    code_snippet=CodeSnippet.objects.get(pk=pk)
    return render(request,'app/detail.html',{'code_snippet':code_snippet})
