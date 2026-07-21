import unittest
from crawl import *
class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    
    def test_normalize_url_2(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    
    def test_normalize_url_capitals(self) -> None:
        input_url = "https://CRAWLER-TEST.com/path"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)
    
    def test_get_header(self):
        input_html = '''
<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>
'''
        expected_header = "Welcome to Boot.dev"
        actual_header = get_heading_from_html(input_html)
        self.assertEqual(actual_header, expected_header)
    
    def test_get_header_no_h1(self):
        input_html = '''
<html>
  <body>
    <h2>Welcome to Boot.dev</h2>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>
'''
        expected_header = "Welcome to Boot.dev"
        actual_header = get_heading_from_html(input_html)
        self.assertEqual(actual_header, expected_header)
    
    def test_get_header_no_h1_or_h2(self):
        input_html = '''
<html>
  <body>
    <main>
      <p>Empty</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>
'''
        expected_header = ""
        actual_header = get_heading_from_html(input_html)
        self.assertEqual(actual_header, expected_header)
    
    def test_get_heading_from_html_with_whitespace(self) -> None:
        input_body = "<html><body><h1>   Whitespace Title   </h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Whitespace Title"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)
    
    def test_get_first_paragraph_from_html_multiple_p(self):
        input_html = '''
<html>
  <body>
    <main>
      <p>First Paragraph</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>
'''
        expected = "First Paragraph"
        actual = get_first_paragraph_from_html(input_html)
        self.assertEqual(actual, expected)
      
    def test_first_paragraph_from_html_no_main(self):
        input_html = '''
<html>
  <body>
      <p>First Paragraph</p>
      <p>This is the second paragraph.</p>
  </body>
</html>
'''
        expected = "First Paragraph"
        actual = get_first_paragraph_from_html(input_html)
        self.assertEqual(actual, expected)
    
    def test_get_first_paragraph_from_html_no_paragraph(self) -> None:
        input_body = "<html><body><h1>No paragraphs here</h1></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_absolute(self):
      input_url = "https://crawler-test.com"
      input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
      actual = get_urls_from_html(input_body, input_url)
      expected = ["https://crawler-test.com"]
      self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_relative(self):
      input_url = "https://crawler-test.com"
      input_body = '<html><body><a href="/funky_wunky"><span>Boot.dev</span></a></body></html>'
      actual = get_urls_from_html(input_body, input_url)
      expected = ["https://crawler-test.com/funky_wunky"]
      self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_multiple_a(self):
      input_url = "https://crawler-test.com"
      input_body = '''
<html>
  <body>
    <h1>Test Page</h1>
    <p>Here are some links:</p>

    <a href="https://crawler-test.com/test_1">Example</a>
    <a href="https://crawler-test.com/test_2">Boot.dev</a>
    <a href="/about">About Us</a>
    <a href="contact.html">Contact</a>
  </body>
</html>
'''
      actual = get_urls_from_html(input_body, input_url)
      expected = ["https://crawler-test.com/test_1", "https://crawler-test.com/test_2", 
                  "https://crawler-test.com/about", "https://crawler-test.com/contact.html"]
      self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
      input_url = "https://crawler-test.com"
      input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
      actual = get_images_from_html(input_body, input_url)
      expected = ["https://crawler-test.com/logo.png"]
      self.assertEqual(actual, expected)

    def test_get_multiple_images_from_html(self):
      input_url = "https://crawler-test.com"
      input_body = '''
<html>
  <body>
    <h1>Image Test Page</h1>

    <img src="cat.png" alt="Cat">
    <img src="/images/dog.jpg" alt="Dog">
    <img src="../assets/fish.gif" alt="Fish">

    <p>Some text between images.</p>

    <img src="photo.jpeg" alt="Photo">
  </body>
</html>
'''
      actual = get_images_from_html(input_body, input_url)
      expected = ["https://crawler-test.com/cat.png", "https://crawler-test.com/images/dog.jpg",
                   "https://crawler-test.com/assets/fish.gif", "https://crawler-test.com/photo.jpeg"]
      self.assertEqual(actual, expected)
    
    
    def test_extract_page_data_basic(self):
      input_url = "https://crawler-test.com"
      input_body = '''<html><body>
          <h1>Test Title</h1>
          <p>This is the first paragraph.</p>
          <a href="/link1">Link 1</a>
          <img src="/image1.jpg" alt="Image 1">
      </body></html>'''
      actual = extract_page_data(input_body, input_url)
      expected = {
          "url": "https://crawler-test.com",
          "heading": "Test Title",
          "first_paragraph": "This is the first paragraph.",
          "outgoing_links": ["https://crawler-test.com/link1"],
          "image_urls": ["https://crawler-test.com/image1.jpg"]
      }
      self.assertEqual(actual, expected)
    
    def test_extract_page_data_multiple_links_and_images(self):
      input_url = "https://crawler-test.com"
      input_body = '''<html><body>
          <h1>Gallery Page</h1>
          <p>Welcome to the gallery.</p>
          <a href="/about">About</a>
          <a href="https://other-site.com/page">External</a>
          <a href="contact.html">Contact</a>
          <img src="/images/photo1.png" alt="Photo 1">
          <img src="banner.jpg" alt="Banner">
      </body></html>'''
      actual = extract_page_data(input_body, input_url)
      expected = {
          "url": "https://crawler-test.com",
          "heading": "Gallery Page",
          "first_paragraph": "Welcome to the gallery.",
          "outgoing_links": [
              "https://crawler-test.com/about",
              "https://other-site.com/page",
              "https://crawler-test.com/contact.html",
          ],
          "image_urls": [
              "https://crawler-test.com/images/photo1.png",
              "https://crawler-test.com/banner.jpg",
          ]
      }
      self.assertEqual(actual, expected)
    
    def test_extract_page_data_main_paragraph_priority(self):
      input_url = "https://crawler-test.com/blog"
      input_body = '''<html><body>
          <p>Outside paragraph.</p>
          <h1>Blog Post</h1>
          <main>
              <p>Main content paragraph.</p>
              <a href="/read-more">Read more</a>
              <img src="/assets/post.jpg" alt="Post image">
          </main>
      </body></html>'''
      actual = extract_page_data(input_body, input_url)
      expected = {
          "url": "https://crawler-test.com/blog",
          "heading": "Blog Post",
          "first_paragraph": "Main content paragraph.",
          "outgoing_links": ["https://crawler-test.com/read-more"],
          "image_urls": ["https://crawler-test.com/assets/post.jpg"]
      }
      self.assertEqual(actual, expected)
    
    def test_extract_page_data_empty_content(self):
      input_url = "https://crawler-test.com/empty"
      input_body = '''<html><body>
          <div>No heading or paragraph here.</div>
      </body></html>'''
      actual = extract_page_data(input_body, input_url)
      expected = {
          "url": "https://crawler-test.com/empty",
          "heading": "",
          "first_paragraph": "",
          "outgoing_links": [],
          "image_urls": []
      }
      self.assertEqual(actual, expected)



if __name__ == "__main__":
    unittest.main()