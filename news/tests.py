from django.test import TestCase
from .models import Editor, Article, tags
import datetime as dt

# Create your tests here.
class EditorTestClass(TestCase):

    def setUp(self):
        self.new_editor = Editor(first_name = 'Lyons', last_name = 'Albert', email = 'lyons@gmail.com')

    #test instance
    def test_instance(self):
        self.assertTrue(isinstance(self.new_editor, Editor))

    def test_save_method(self):
        self.new_editor.save_editor()
        editors = Editor.objects.all()
        self.assertTrue(len(editors) > 0)

class ArticleTestClass(TestCase):
# Here we create a test class ArticleTestClass to test our Article model. We create the setUp method that allows us to define a new Editor and tag instance.
# Since the Editor and Article share a One to Many relationship we have to save the editor instance first then equate it to the editor field in the Article model.
# The Article and tags share a Many to Many relationship. This means for us to create a join table we need the id property of both model instances. So first, we save
# both the tags and article instance to the database then we use the add function on the ManyToManyField to add a new tag.
# We also define a tearDown method that will allow us to delete all instances of our models from the database after each test.

    def setUp(self):
        # Creating a new editor and saving it
        self.james= Editor(first_name = 'James', last_name ='Muriuki', email ='james@moringaschool.com')
        self.james.save_editor()

        # Creating a new tag and saving it
        self.new_tag = tags(name = 'testing')
        self.new_tag.save()

        self.new_article= Article(title = 'Test Article',post = 'This is a random test Post',editor = self.james)
        self.new_article.save()

        self.new_article.tags.add(self.new_tag)

    def tearDown(self):
        Editor.objects.all().delete()
        tags.objects.all().delete()
        Article.objects.all().delete()

    def test_get_news_today(self):
        today_news = Article.today_news()
        self.assertTrue(len(today_news) > 0)

    def test_get_news_by_date(self):
        test_date = '2022-03-10'
        date = dt.datetime.strptime(test_date, '%Y-%m-%d').date()
        news_by_date = Article.days_news(date)
        self.assertTrue(len(news_by_date) == 0)