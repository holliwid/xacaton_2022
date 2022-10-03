using Microsoft.EntityFrameworkCore;
using Server.Models;
namespace Server
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);
            string connection = builder.Configuration.GetConnectionString("DefaultConnection");
            builder.Services.AddDbContext<DataContext>(options => options.UseSqlServer(connection));
            builder.Services.AddControllers();
            var app = builder.Build();
            app.MapControllers();
            app.Run();
        }
    }
}