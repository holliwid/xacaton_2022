using Desktop.Views;
using System.Windows;
namespace Desktop
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }
        /// <summary>
        /// Страница с происшествиями
        /// </summary>
        private void GetReportList(object sender, RoutedEventArgs e)
        {
            MainFrame.Navigate(new ReportPage());
        }
        /// <summary>
        /// Страница с нейронной сетью
        /// </summary>
        private void NeuralNetworkSettings(object sender, RoutedEventArgs e)
        {
            MainFrame.Navigate(new AIPage());
        }
    }
}