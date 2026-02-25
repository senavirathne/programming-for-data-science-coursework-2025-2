
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import scraper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import scraper

class TestScraper(unittest.TestCase):

    @patch('question2_ecommerce_analysis.scraper.session.get')
    def test_get_soup_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"<html><body><h1>Test</h1></body></html>"
        mock_get.return_value = mock_response
        
        soup = scraper.get_soup("http://test.com")
        self.assertIsNotNone(soup)
        self.assertEqual(soup.h1.text, "Test")

    @patch('question2_ecommerce_analysis.scraper.session.get')
    def test_get_soup_failure(self, mock_get):
        mock_get.side_effect = scraper.requests.exceptions.RequestException("Error")
        
        soup = scraper.get_soup("http://test.com")
        self.assertIsNone(soup)

    @patch('question2_ecommerce_analysis.scraper.get_soup')
    def test_scrape_book_details(self, mock_get_soup):
        # Mock HTML content for a book page
        html = """
        <div class="product_main">
            <h1>A Light in the Attic</h1>
            <p class="price_color">£51.77</p>
            <p class="star-rating Three"></p>
            <p class="instock availability">In stock (22 available)</p>
        </div>
        <ul class="breadcrumb">
            <li><a href="index.html">Home</a></li>
            <li><a href="books_1/index.html">Books</a></li>
            <li><a href="poetry_23/index.html">Poetry</a></li>
            <li class="active">A Light in the Attic</li>
        </ul>
        """
        mock_soup = MagicMock()
        mock_soup.find.return_value = BeautifulSoup(html, 'html.parser').find("div", class_="product_main")
        # Creating a real soup and mocking find behavior is tricky with MagicMock.
        # Better to return a real BeautifulSoup object.
        mock_get_soup.return_value = BeautifulSoup(html, 'html.parser')

        details = scraper.scrape_book_details("http://test.com/book")
        
        self.assertEqual(details['Title'], "A Light in the Attic")
        self.assertEqual(details['Price'], "£51.77")
        self.assertEqual(details['Rating'], "Three")
        self.assertEqual(details['Category'], "Poetry")
        self.assertIn("In stock", details['Availability'])

if __name__ == '__main__':
    unittest.main()
