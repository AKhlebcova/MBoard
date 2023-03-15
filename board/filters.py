from django_filters import FilterSet, ModelMultipleChoiceFilter
from .models import Post, Feedback


def get_post_queryset(request):
    queryset = Post.objects.filter(author=request.user)
    return queryset


class FeedFilter(FilterSet):
    feedpost = ModelMultipleChoiceFilter(
        field_name='post__title',
        queryset=get_post_queryset,
        label='Заголовок',
    )

    class Meta:
        model = Feedback
        fields = [
            'feedpost',
        ]
