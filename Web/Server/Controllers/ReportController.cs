using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Server.Models;
using Newtonsoft.Json;
namespace Server.Controllers
{
    [Controller]
    [Route("Report")]
    public sealed class ReportController : Controller
    {
        private readonly DataContext db;
        public ReportController(DataContext context) => db = context;
        /// <summary>
        /// Получение списка происшествий из БД
        /// </summary>
        /// <returns>Список происшествий</returns>
        [HttpGet]
        [Route("Get/{id:int}")]
        public string GetReports(int id)
        {
            Console.WriteLine($"Current path: {Request.Path}");
            return JsonConvert.SerializeObject(db.Reports.FromSqlRaw<Report>(
            @$"select R.ID, R.Photo, D.Name, R.Date, R.Time, ET.Description Description, D.Name Department from Departments D
	            right join Reports R on D.ID = R.Depart_ID
	            left join EventTypes ET on ET.ID = R.Event_ID
            where R.ID={id}
            order by R.Date desc, R.Time desc").ToList(), Formatting.Indented);
        }

        /// <summary>
        /// Добавить новый репорт в БД
        /// </summary>
        /// <param name="report"></param>
        [HttpPost]
        [Route("Add")]
        public void AddReport(Report report)
        {
            //db.Reports.Add(report);
            //db.SaveChanges();
        }
    }
}