using Desktop.Models;
using System.IO;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Media.Imaging;
namespace Desktop.Views
{
    public partial class ReportControl : UserControl
    {
        private readonly Report _report;

        /// <summary>
        /// Фото происшествия
        /// </summary>
        public ImageSource ReportPhoto => miniPhoto.Source;

        /// <summary>
        /// Описание происшествия
        /// </summary>
        public string ReportDesctiption => _report.Description;

        /// <summary>
        /// Время происшествия
        /// </summary>
        public int ReportTime => _report.Time;

        /// <summary>
        /// Мини-репорт
        /// </summary>
        /// <param name="report">Репорт</param>
        public ReportControl(Report report)
        {
            InitializeComponent();
            _report = report;
            miniPhoto.Source = BitmapFrame.Create(
                new MemoryStream(_report.Photo),
                BitmapCreateOptions.None,
                BitmapCacheOption.OnLoad);
        }
    }
}