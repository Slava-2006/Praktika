from django.db import models


class SearchQuery(models.Model):
    city = models.CharField(max_length=100, blank=True, null=True)
    time_type = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    skills = models.CharField(max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SearchQuery(id={self.id}, city={self.city}, job_title={self.job_title})"


class Vacancy(models.Model):
    search_query = models.ForeignKey(SearchQuery, related_name='vacancies', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    treb = models.TextField()
    link = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vacancy(id={self.id}, title={self.title}, company_name={self.company_name})"
