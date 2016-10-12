from django.test import TestCase
from core.models import Category,Business,ParentCategory
from django.test import Client
from django.core.urlresolvers import reverse,resolve
from django.shortcuts import get_object_or_404
import json

# Create your tests here.

class AdminTest(TestCase):
    
    fixtures = ['core/fixtures/initial_data.json']
    def setUp(self):
        self.cat1=Category.objects.create(name="cat1",)
        self.cat2=Category.objects.create(name="cat2",)
        self.cat3=Category.objects.create(name="dog",)
        self.business=Business.objects.create(name="biz")
        self.parent_cat=ParentCategory.objects.create(name="parent",icon="icon")
        self.cat1.parent_category = self.parent_cat
        self.cat2.parent_category = self.parent_cat
        self.cat3.parent_category = self.parent_cat
        self.cat1.save()
        self.cat2.save()
        self.cat3.save()

    def test_get_categories(self):
        response = self.client.get(reverse('admin:get_categories'), {'query':'ca'})
        self.assertEquals(response.status_code, 200)
        print response.content

    def test_can_add_business(self):
        response = self.client.post('/manager/create_business/',{'name':'javas'})
        self.assertEquals(response.status_code,302)
        self.assertEquals(response['Location'],'http://testserver/manager/business_manage_photos/')

    def test_can_delete_business(self):
        business = Business.objects.get(name='biz')
        response = self.client.delete(reverse('admin:delete_business',kwargs={'pk':business.pk}))
        self.assertEquals(response.status_code,302)

    def test_can_edit_business(self):
        business = Business.objects.get(name='biz')
        response = self.client.post(reverse('admin:update_business',kwargs={'pk':business.pk}),{'name':'edited'})
        business= Business.objects.get(pk=business.pk)
        self.assertEquals(business.name,'edited')

    def test_can_save_parent_categories_ajax(self):
        response = self.client.post('/manager/create_parent_category/',{'name':'harold'})
        parent_category = ParentCategory.objects.get(name='harold')
        self.assertEquals(response.status_code,200)
        self.assertJSONEqual(str(response.content),{'name':parent_category.name,'id':parent_category.pk})

    def test_can_delete_parent_category(self):
        response = self.client.post('/manager/delete_parent_category/',{'id':self.parent_cat.pk})
        self.assertEquals(response.status_code,200)

    def test_can_edit_parent_category(self):
        parent_cat = ParentCategory.objects.create(name="parent")
        response = self.client.post('/manager/update_parent_category/',{'id':parent_cat.pk,'name':'changed_parent'})
        changed_cat = get_object_or_404(ParentCategory,pk=parent_cat.pk)
        self.assertEquals(response.status_code,200)
        self.assertJSONEqual(str(response.content),{'name':changed_cat.name,'id':changed_cat.pk})
        print response.content

    def test_can_add_sub_category(self):
        response = self.client.post('/manager/create_sub_category/',{'name':'sub','parent_category_id':self.parent_cat.pk,'icon':'icon'})
        category = get_object_or_404(Category,name='sub')
        self.assertJSONEqual(str(response.content),{'name':category.name,'icon':category.icon,
                                                    'parent_category_id':self.parent_cat.pk,'sub_category_id':category.pk})
        print response.content

    def test_can_edit_sub_category(self):
        response = self.client.post('/manager/edit_sub_category/',{'name':'edit_sub','icon':'edit_icon','parent_id':self.parent_cat.id,
                                                                   'id':self.cat1.pk})
        self.assertEquals(response.status_code,200)
        print response.content

    def test_can_delete_sub_category(self):
        response = self.client.post('/manager/delete_sub_category/',{'id':self.cat1.pk})
        self.assertEquals(response.status_code,200)
        self.assertJSONEqual(str(response.content),{'success':'true'})

    def test_can_upload_business_images(self):
        image_list=[]
        photo1 = open('E:/workspace/africa_one/africa_one/media/businesses/2016/01/15/1017_1_1.jpg')
        photo2 = open('E:/workspace/africa_one/africa_one/media/businesses/2016/01/15/1017_2.jpg')
        image_list.append(photo1)
        image_list.append(photo2)
        response = self.client.post('/manager/upload_business_photos/',{'photos':image_list,'business_id':self.business.pk})
        self.assertEquals(response.status_code,200)
        print response.content


    def test_can_delete_logo(self):
        photo = open('E:/workspace/africa_one/africa_one/media/businesses/2016/01/15/1017_1_1.jpg')
        self.business.photo = photo
        self.business.save()
        response = self.client.post('/manager/delete_business_logo/',{'business_id':self.business.pk})
        self.assertEquals(response.status_code,200)
        self.assertEquals(self.business.photo,None)



    def test_get_categories(self):
        response = self.client.get('/manager/get_all_categories/',)
        self.assertEquals(response.status_code,200)
        print response.content

















