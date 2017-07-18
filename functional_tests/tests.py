from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException 
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()
	
	def wait_for_row_in_list_table(self, row_text):
		
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return 
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)
	
	def test_can_start_a_list_for_one_user(self):
		#Edith has heard about a cool new online to-do app.
		# She goes to check out its homepage
		self.browser.get(self.live_server_url)

		#She notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		#She is invited to enter a to-do item straight away	
		input_box = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			input_box.get_attribute('placeholder'),
			'Enter a to-do item'
			)
		
		#She types "Buy peacock feathers" into a text box
		input_box.send_keys('Buy peacock feathers')
		input_box.send_keys(Keys.ENTER)

		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		#There is still a text box inviting her to add another item. 
		#She enters "Use peacock feathers to make a fly" 
		input_box = self.browser.find_element_by_id('id_new_item')
		input_box.send_keys('Use peacock feathers to make a fly')
		input_box.send_keys(Keys.ENTER)

		# Edith wonders whether the site will remember her list. Then she sees
		# that the site has generated a unique URL for her -- there is some
		# explanatory text to that effect.
		self.wait_for_row_in_list_table(u'2: Use peacock feathers to make a fly')
		self.wait_for_row_in_list_table(u'1: Buy peacock feathers')
		

	def test_multiple_users_can_start_lists_at_different_urls(self):
		self.browser.get(self.live_server_url)
		input_box = self.browser.find_element_by_id('id_new_item')
		input_box.send_keys('Buy peacock feathers')
		input_box.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		#New user Francis
		self.browser.quit()
		self.browser = webdriver.Firefox()

		#Make sure Edith's list isn't viewable 
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		#Francis starts his own list
		input_box = self.browser.find_element_by_id('id_new_item')
		input_box.send_keys('Buy milk')
		input_box.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		#Francis get his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		#Again, there is no trace of Edith's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)












