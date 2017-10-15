from app.business.models import Category, Country, City, Business, Feature

# adding categories
categories = ['Restaurant', 'Automotive', 'Shopping', 'Services', 'Hotels', 'Entertainment']
for cat in categories:
    Category(name=cat).save()


## adding country
countries = [['IN', 'India'], ['USA', 'United Status of America'], ['RS', 'Russia'], ['CH', 'China']]
for country in countries:
    Country(name=country[1], code=country[0]).save()


cities = {'IN': ['Delhi', 'Lucknow', 'Mumbai', 'Gurgaon'],
          'USA': ['Alaska', 'New York']}

for country in cities:
    for city in cities[country]:
        ct = Country.objects.get(code=country)
        City(name=city, country=ct).save()


features = ['Feature1', 'Feature2', 'Feature3', 'Feature4']
for feature in features:
    Feature(name=feature).save()