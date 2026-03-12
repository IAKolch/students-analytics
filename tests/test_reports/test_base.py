import pytest

from reports.base import Report, ReportFactory


class TestReportFactoryWithMocks:
    
    def setup_method(self):
        ReportFactory._reports = {}
    
    def test_register_creates_instance_to_get_name(self, mocker):
        """Тест что register создает экземпляр для получения name"""

        mock_report_class = mocker.MagicMock()
        mock_instance = mocker.MagicMock()
        mock_instance.name = "mock-report"
        mock_report_class.return_value = mock_instance
        
        ReportFactory.register(mock_report_class)
        
        mock_report_class.assert_called_once_with()
        assert ReportFactory._reports["mock-report"] == mock_report_class
    
    def test_create_instantiates_report_class(self, mocker):
        """Тест что create создает экземпляр зарегистрированного класса"""

        mock_report_class = mocker.MagicMock()
        mock_report_instance = mocker.MagicMock(spec=Report)
        mock_report_class.return_value = mock_report_instance
        
        ReportFactory._reports = {"mock-report": mock_report_class}
        
        report = ReportFactory.create("mock-report")
        
        mock_report_class.assert_called_once_with()
        assert report == mock_report_instance
    
    
    def test_create_unknown_report_error_message(self, mocker):
        """Тест сообщения об ошибке для неизвестного отчета"""

        ReportFactory._reports = {
            "report1": mocker.MagicMock(),
            "report2": mocker.MagicMock()
        }
        
        with pytest.raises(ValueError):
            ReportFactory.create("unknown")
