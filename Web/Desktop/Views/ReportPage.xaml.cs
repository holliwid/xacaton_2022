using Desktop.Models;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Controls;
namespace Desktop.Views
{
    /// <summary>
    /// Страница с происшествиями
    /// </summary>
    public partial class ReportPage : Page
    {
        /// <summary>
        /// БД происшествий
        /// </summary>
        private readonly DataContext _db = new();
        public ReportPage()
        {
            InitializeComponent();
        }
        private void Page_Loaded(object sender, System.Windows.RoutedEventArgs e)
        {
            List<Report> repList = _db.Reports.FromSqlRaw(
                @$"select R.ID ID, R.Photo Photo, D.Name Department, R.Time, ET.Description Description from Departments D
	                right join Reports R on D.ID = R.Depart_ID
	                left join EventTypes ET on ET.ID = R.Event_ID
                order by R.Time desc").ToList<Report>();
            foreach(Report report in repList)
            {
                ReportControl reportControl = new ReportControl(report);
                reportList.Items.Add(reportControl);
            }
        }
        private void reportList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            ReportControl currentReport = (ReportControl)((ListBox)sender).SelectedItem;
            ReportTime.Text = currentReport.ReportTime.ToString();
            ReportImage.Source = currentReport.ReportPhoto;
            ReportText.Text = currentReport.ReportDesctiption;
        }
    }
}