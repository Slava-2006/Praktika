from django.shortcuts import render, get_object_or_404
from bs4 import BeautifulSoup
from .models import SearchQuery, Vacancy
import requests


city_codes = {
    "c_685": "Белгород",
    "c_690": "Волгоград",
    "c_692": "Воронеж",
    "c_696": "Иркутск",
    "c_698": "Казань",
    "c_699": "Калининград",
    "c_700": "Калуга",
    "c_710": "Курсk",
    "c_712": "Липецк",
    "c_715": "Нижний Новгород",
    "c_716": "Новокузнецк",
    "c_718": "Омск",
    "c_719": "Орел",
    "c_720": "Оренбург",
    "c_724": "Псков",
    "c_726": "Ростов-На-Дону",
    "c_737": "Тула",
    "c_740": "Уфа",
    "c_741": "Хабаровск",
    "c_743": "Чебоксары",
    "c_746": "Якутск",
}

def main(request):       
    return render(request, 'index.html')



def vacancies_by_search_query(request, search_query_id):
    search_query = get_object_or_404(SearchQuery, id=search_query_id)
    vacancies = search_query.vacancies.all()
    return render(request, 'vacancies_by_search_query.html', {'vacancies': vacancies, 'search_query': search_query})

def search_history(request):
    search_queries = SearchQuery.objects.all().order_by('-timestamp')
    return render(request, 'search_history.html', {'search_queries': search_queries})

def advanced_search(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        time_type = request.POST.get('time_type')
        company = request.POST.get('company')
        job_title = request.POST.get('job_title')
        skills = request.POST.get('skills')

        search_query = SearchQuery.objects.create(
            city=city_codes.get(city),
            time_type=time_type,
            company=company,
            job_title=job_title,
            skills=skills
        )
        
        url = 'https://career.habr.com/vacancies?'
        if city:
            url += f'&locations[]={city}'
        if time_type:
            url += f'&employment_type={time_type}'
        if job_title:
            url += f'&q={job_title}'
        
        url += f'&type=all'

        response = requests.get(url)

        html_content = response.text

        soup = BeautifulSoup(html_content, "html.parser")

        vacancy = soup.find_all("div", class_="vacancy-card")
        count = 0
        filtered_vacancies = []
        
        for element in vacancy:
            company_name = element.find("div", class_="vacancy-card__company").text.strip()
            title = element.find("div", class_="vacancy-card__title").text.strip()
            place = element.find("div", class_="vacancy-card__meta").text.strip()
            treb = element.find("div", class_="vacancy-card__skills").text.strip()
            link = "https://career.habr.com" + element.find("div", class_="vacancy-card__title").a['href']

            matches = True
            if company and company.lower() not in company_name.lower():
                matches = False
            if skills and skills.lower() not in treb.lower():
                matches = False

            if matches:
                # Сохранение вакансии
                vacancy = Vacancy.objects.create(
                    search_query=search_query,
                    title=title,
                    company_name=company_name,
                    place=place,
                    treb=treb,
                    link=link
                )

                filtered_vacancies.append({
                    'company_name': company_name,
                    'title': title,
                    'place': place,
                    'treb': treb,
                    'link': link,
                })
                count += 1
            
        
        context = {
            'filtered_vacancies': filtered_vacancies,
            'count': count
        }

        return render(request, 'search_results.html', context)
                
        
        
