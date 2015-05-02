from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item

# Create your tests here.

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')    

    def test_display_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
      
        response = self.client.get('/lists/the-only-list-in-the-world/') #
        
        self.assertContains(response, 'itemey 1') #
        self.assertContains(response, 'itemey 2')     

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        t=('The first ever item.', 'The second item now$.', '%#LXED KL thrid')
        for text in t:
            it = Item()
            it.text = text
            it.save()
        noit = Item.objects.all() 
        self.assertEqual(len(noit),len(t))
        
        for i,tt in enumerate(t):
            self.assertEqual(noit[i].text,tt)
            
 

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
        t='A new list item'
        request=HttpRequest()
        request.method='POST'
        request.POST['item_text'] = t
        #do-it
        response=home_page(request)
        #assert
        #first via Item
        self.assertEqual(Item.objects.count(),1) # should have 1 item
        new_item=Item.objects.first()
        self.assertEqual(new_item.text,t)        
        
    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')        
        
    def test_home_page_only_saves_items_when_necessary_ie_POSTed(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)
 
        
    def _test_home_page_only_saves_items_when_non_empty(self):
        request = HttpRequest()
        request.method="POST"
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)
        request.POST['item_text'] = None
        self.assertEqual(Item.objects.count(), 0)
        request.POST['item_text'] = ''
        self.assertEqual(Item.objects.count(), 0)   
        
    ### Duplicate test now.     ListViewTest.test_display_all_list_items 
    ### does the same via the new URL scheme. 
    #def test_home_page_displays_all_list_items(self):
        #Item.objects.create(text='itemey 1')
        #Item.objects.create(text='itemey 2')
        #request = HttpRequest()
        #response = home_page(request)
        #self.assertIn('itemey 1', response.content.decode())
        #self.assertIn('itemey 2', response.content.decode())        