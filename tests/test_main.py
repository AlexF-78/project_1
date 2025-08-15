import os
import sys
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main


def test_main_execution():
    with patch('main.generate_full_report') as mock_func:
        mock_func.return_value = "test output"
        main()
        mock_func.assert_called_once_with("2019-11-25 14:30:00")
