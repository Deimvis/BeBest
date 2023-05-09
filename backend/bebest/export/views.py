from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from posts.models import Post
from .forms import ExportPostsForm
from .models import DatacampPost, ExportLog


def _export_posts() -> dict:
    Post.objects.all().delete()
    for datacamp_post in DatacampPost.objects.all():
        post = Post(
            canonized_url = datacamp_post.canonized_url,
            source_name = datacamp_post.source_name,
            original_url = datacamp_post.original_url,
            title = datacamp_post.title,
            topics = datacamp_post.topics,
            rank = datacamp_post.rank,
            starting_text = datacamp_post.starting_text,
            publish_timestamp = datacamp_post.publish_timestamp,
            author_username = datacamp_post.author_username,
            views = datacamp_post.views,
        )
        post.save()
    timestamp = int(timezone.now().timestamp())  # UTC
    ExportLog(
        source_table_name = DatacampPost.objects.model._meta.db_table,
        destination_table_name = Post.objects.model._meta.db_table,
        timestamp = timestamp,
    ).save()
    return {
        'status': 'Done',
        'timestamp': timestamp,
    }


def index(request):
    def beautify(log_dict: dict) -> str:
        iso_dateteime = datetime.utcfromtimestamp(log_dict['timestamp']).isoformat()
        return f'{iso_dateteime} | {log_dict["destination_table_name"]} <— {log_dict["source_table_name"]}'

    logs = ExportLog.objects.order_by('-timestamp')
    return HttpResponse('Index' + '<br>' + '<br>'.join(map(lambda log: beautify(model_to_dict(log)), logs)))


@staff_member_required
@transaction.atomic
def export_posts(request):
    if request.method == 'POST':
        form = ExportPostsForm(request.POST)
        if form.is_valid():
            _export_posts()
            return HttpResponseRedirect(reverse('export:index'))
    else:
        form = ExportPostsForm()
    return render(request, 'export/export_posts.html', {'form': form})

# transactional swap
# https://dba.stackexchange.com/a/100787
