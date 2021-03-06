from process import GetBookAuthor
import unittest
from mock import MagicMock, patch, ANY, call
from mod_11_testing.library import ConnectionError


class TestGetAllBookAuthor(unittest.TestCase):
    """
    Test class for get_info_list method of GetBookAuthor.
    We will increase coverage of this method.
    We do not inheritate for TestCase as we dont want to be
    discovered by nosetests, just for checking
    """

    def test_get_all_books_work(self):
        """
        When database module is working we check that our process return a valid list
        """
        with patch('modules.exercises.mod_11_testing.process.MyConnection') as con_class:
            mock_db = MagicMock(name='db_mock')
            con_class.return_value = mock_db
            mock_db.get_book.side_effect = [
                                    {"book_id": "10", "author_name": "test__another_1", "name": "name_1"},
                                    {"book_id": "11", "author_name": "test__another_2", "name": "name_2"},
                            ]
            # Two books with the same author, we suppose that
            mock_db.get_author.return_value = {"name": "name_another_mock", "age": -10, "best_sellers": -50}

            # call the method
            get_book = GetBookAuthor()
            data = get_book.get_info_list(10, 11)

            # asserts
            mock_db.get_book.assert_has_calls([call(10), call(11)])
            mock_db.get_author.assert_has_calls([call(ANY), call(ANY)])
            self.assertEquals(2, len(data))
            self.assertEquals("name_1", data[0]['title'])
            self.assertEquals("name_2", data[1]['title'])

    def test_get_all_books_failing_db(self):
        """
        TEst that database error is handled in our process module and we dont raise any exception up
        """
        with patch('modules.exercises.mod_11_testing.process.MyConnection') as con_class,\
            patch('modules.exercises.mod_11_testing.process.logger') as logger_mock:
            mock_db = MagicMock(name='db_mock')
            con_class.return_value = mock_db
            mock_db.get_book.side_effect = [
                                    {"book_id": "10", "author_name": "test__another_1", "name": "name_1"},
                                    {"book_id": "11", "author_name": "test__another_2", "name": "name_2"},
                            ]
            # Two books with the same author, we suppose that
            mock_db.get_author.side_effect = ConnectionError("authors collection not created")

            # call the method
            get_book = GetBookAuthor()
            data = get_book.get_info_list(10, 11)

            # asserts
            mock_db.get_book.assert_called_once_with(10)
            mock_db.get_author.assert_called_once_with(ANY)
            self.assertEquals(0, len(data))

            # logger is not called with constructor, so we access mock method directly
            logger_mock.error.assert_called_once_with("Conection with database lost")
