using Microsoft.EntityFrameworkCore;
namespace Server.Models
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
        public DataContext(DbContextOptions<DataContext> options) : base(options) { }
    }
}