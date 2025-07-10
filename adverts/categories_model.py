import os
import django
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Set your Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pomo6.settings")

# Setup Django
django.setup()

from adverts.models import Advertisement

advert_titles = list(Advertisement.objects.all().values_list('title', flat=True))
advert_categories = list(Advertisement.objects.all().values_list('category', flat=True))

x_train, x_test, y_train, y_test = train_test_split(advert_titles, advert_categories,
                                                    test_size=0.2,
                                                    random_state=42,
                                                    stratify=advert_categories)


vectorizer = TfidfVectorizer()
x_vec_train = vectorizer.fit_transform(x_train)
x_vec_test = vectorizer.transform(x_test)


model = MultinomialNB()
model.fit(x_vec_train, y_train)

y_pred = model.predict(x_vec_test)
print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

joblib.dump(vectorizer, '../ml_model/vectorizer.pkl')
joblib.dump(model, '../ml_model/model.pkl')