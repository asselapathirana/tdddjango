from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List

# Create your tests here.

class NewListTest(TestCase):
    def test_saving_POST_request(self):
        self.client.post(
        '/lists/new',
        data={'item_text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')                
        
    def test_redirects_after_POST(self):
        response = self.client.post(
        '/lists/new',
        data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
    

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.post(   '/lists/new',
            data={'item_text': 'A new list item'})
        new_list = List.objects.first()        
        response = self.client.get('/lists/%d/' % (new_list.id))
        self.assertTemplateUsed(response, 'list.html')    

    def test_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)        
      
        response = self.client.get('/lists/%d/' % (correct_list.id,)) #
        
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')     

class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()
        
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()
        

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
    
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)        
 

class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found=resolve('/')
        
        self.assertEqual(found.func,home_page)
        
    def test_home_page_returns_correct_html_page(self):
        request=HttpRequest()
        response=home_page(request)
        expected=render_to_string('home.html')
        self.assertEqual(response.content.decode(),expected)
        
        
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