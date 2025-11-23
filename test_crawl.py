import unittest
from crawl import (
    extract_page_data,
    get_first_paragraph_from_html,
    get_h1_from_html,
    get_images_from_html,
    get_urls_from_html,
    normalize_url,
)


class TestCrawl(unittest.TestCase):
    def test_normalize_url_1(self):
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_2(self):
        input_url = "https://blog.boot.dev"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev"
        self.assertEqual(actual, expected)

    def test_normalize_url_3(self):
        input_url = None
        actual = normalize_url(input_url)
        expected = None
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_1(self):
        html = "<html><body><h1>Welcome to Boot.dev</h1></body></html>"
        actual = get_h1_from_html(html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_no_h1(self):
        html = "<html><body></body></html>"
        actual = get_h1_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_nested(self):
        html = "<html><body><h1>Hi <span>there</span></h1></body></html>"
        actual = get_h1_from_html(html)
        expected = "Hi there"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html(self):
        html = """
        <html>
          <body>
            <h1>Welcome to Boot.dev</h1>
              <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
              </main>
          </body>
        </html>
        """
        actual = get_first_paragraph_from_html(html)
        expected = "Learn to code by building real projects."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_not_equal_first(self):
        html = """
        <html>
          <body>
            <p>This is the second paragraph.</p>
            <p>Learn to code by building real projects.</p>
          </body>
        </html>
        """
        actual = get_first_paragraph_from_html(html)
        expected = "Learn to code by building real projects."
        self.assertNotEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_paragraph(self):
        html = "<html><body><h1>Welcome to Boot.dev</h1></body></html>"
        actual = get_first_paragraph_from_html(html)
        print(actual)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_links_from_html_absolute_url(self):
        html = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        base_url = "https://blog.boot.dev"
        actual = get_urls_from_html(html, base_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)

    def test_get_links_from_html_relative_url(self):
        html = '<html><body><a href="/path"><span>Boot.dev</span></a></body></html>'
        base_url = "https://blog.boot.dev"
        actual = get_urls_from_html(html, base_url)
        expected = ["https://blog.boot.dev/path"]
        self.assertEqual(actual, expected)

    def test_get_links_from_html_none_attribute(self):
        html = """
        <html>
          <body>

            <a>Go to Boot.dev (broken link)</a>
            <img src="/logo.png" alt="Boot.dev Logo" />

            <a href="https://blog.boot.dev">Go to Boot.dev</a>
            <img src="/logo.png" alt="Boot.dev Logo" />

          </body>
        </html>
        """
        base_url = "https://blog.boot.dev"
        actual = get_urls_from_html(html, base_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative_none_src(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative_2(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"><img src="/logo2.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png", "https://blog.boot.dev/logo2.png"]
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic_1(self):
        input_url = "https://blog.boot.dev"
        input_body = """
        <html>
          <body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
          </body>
        </html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic_2(self):
        input_url = "https://blog.boot.dev"
        input_body = """
        <html>
          <body>
            <h1><span>Test Title</span></h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
            <a href="/link2">Link 2</a>
            <img src="/image2.jpg" alt="Image 2">
          </body>
        </html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": [
                "https://blog.boot.dev/link1",
                "https://blog.boot.dev/link2",
            ],
            "image_urls": [
                "https://blog.boot.dev/image1.jpg",
                "https://blog.boot.dev/image2.jpg",
            ],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic_3(self):
        input_url = "https://blog.boot.dev"
        input_body = """
        <html>
          <body>
            <h1><span>Test Title</span></h1>
            <p>This is the first paragraph.</p>
          </body>
        </html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic_4(self):
        input_url = "https://blog.boot.dev"
        input_body = """
        <html>
          <body>
            <h1><span>Test Title</span></h1>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
            <a href="/link2">Link 2</a>
            <img src="/image2.jpg" alt="Image 2">            
          </body>
        </html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "",
            "outgoing_links": [
                "https://blog.boot.dev/link1",
                "https://blog.boot.dev/link2",
            ],
            "image_urls": [
                "https://blog.boot.dev/image1.jpg",
                "https://blog.boot.dev/image2.jpg",
            ],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic_5(self):
        input_url = "https://blog.boot.dev"
        input_body = """
        <html>
          <body>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
            <a href="/link2">Link 2</a>
            <img src="/image2.jpg" alt="Image 2">            
          </body>
        </html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "",
            "first_paragraph": "",
            "outgoing_links": [
                "https://blog.boot.dev/link1",
                "https://blog.boot.dev/link2",
            ],
            "image_urls": [
                "https://blog.boot.dev/image1.jpg",
                "https://blog.boot.dev/image2.jpg",
            ],
        }
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
