from .serializers import ArticleSerializer
from .models import Article
from rest_framework import viewsets

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-published_date')
    serializer_class = ArticleSerializer
    
    # Filtracja według źródła (domeny) w URL
    def get_queryset(self):
        queryset = super().get_queryset()
        source = self.request.query_params.get("source")
        if source:
            queryset = queryset.filter(url__icontains=source)
        return queryset