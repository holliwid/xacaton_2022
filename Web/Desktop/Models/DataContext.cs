using Microsoft.EntityFrameworkCore;
namespace Desktop.Models
{
    /// <summary>
    /// Модель взаимодействия с БД происшествий
    /// </summary>
    public sealed class DataContext : DbContext
    {
        /// <summary>
        /// Коллекция объектов-репортов
        /// </summary>
        public DbSet<Report> Reports { get; set; }
        protected override void OnConfiguring(DbContextOptionsBuilder options)
        {
            options.UseSqlServer("Server=DESKTOP-71PDH2V;Database=Reports;Trusted_Connection=True;");
        }
    }
}