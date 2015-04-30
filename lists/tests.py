from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

# Create your tests here.
class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found=resolve('/')
        
        self.assertEqual(found.func,home_page)
        
    def test_home_page_returns_correct_html_page(self):
        request=HttpRequest()
        response=home_page(request)
        expected=render_to_string('home.html')
        self.assertEqual(response.content.decode(),expected)
        
    def test_home_page_can_save_a_POST_request(self):
        #Setup
        request=HttpRequest()
        request.method='POST'
        request.POST['item_text'] = 'A new list item'
        #do-it
        response=home_page(request)
        #assert
        self.assertIn("A new list item", response.content.decode())
          #now directly render home.html with the valueset.
        expected = render_to_string('home.html',{'new_item_text': 'A new list item'})
          #is the response of home_page equal to this?
        print (response.content.decode())
        self.assertEqual(response.content.decode(), expected)