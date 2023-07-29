from django.shortcuts import render,get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator,EmptyPage
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.http import Http404

# Create your views here.

def post_list(request, tag_slug =None):
    post_list = Post.published.all()
    tag =None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list,6)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except:
        #if page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
        
    context = {
    'posts':posts,
    'tag':tag,
    'apost':post_list,
    'last_three_posts' : Post.published.all().order_by('-id')[:6],
    'last_four_posts' : Post.published.all().order_by('-id')[:4],
    }
    return render(request,'post/post_list.html',context)



def post_detail(request,year,month,day,slug):
    # Hard Code
    # try:
    #     post=Post.published.get(id=id)

    # except Post.DoesNotExist:
    #     raise Http404("No Post Found!")
   

    post = get_object_or_404(Post,
                             status =Post.Status.PUBLISHED,
                              slug=slug,
                              publish__year =year,
                              publish__month=month,
                              publish__day = day)
    # List of active comments for this post
    comments = post.comments.filter(active = True)
    # Form for users to comment
    form = CommentForm()
    
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in = post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags =Count('tags'))\
                                 .order_by('-same_tags','-publish')[:4]

    return render (request,'post/post_detail.html',{'post':post,
                                                    'comments':comments,
                                                    'form':form,
                                                    'similar_posts':similar_posts})








def post_share(request,post_id):
    # Retrieve post by id
    post = get_object_or_404(Post,
                             id =post_id,
                             status=Post.Status.PUBLISHED)
    sent = False
    
    if request.method == 'POST':
        # Form was sumbitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'aabdualwasaa11@gmail.com',
                      [cd['to']])
            sent = True
            
    else:
        form = EmailPostForm()
    return render(request, 'post/share.html', {'post':post,
                                                    'form':form,
                                                    'sent':sent})


@require_POST
def post_comment(request,post_id):
    post = get_object_or_404(Post,
                             id = post_id,
                             status = Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object wuthout saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render (request, 'post/comment.html',
                            {'post':post,
                             'form':form,
                             'comment':comment})
    
    
    
def about (request):
    return render(request,'post/about.html')
    
    
