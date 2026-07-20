import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html

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

    



if __name__ == "__main__":
    unittest.main()