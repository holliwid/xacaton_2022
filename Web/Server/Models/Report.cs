using Newtonsoft.Json;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Data.SqlTypes;
using System.Text.Json.Serialization;
namespace Server.Models
{
    /// <summary>
    /// Доклад о происшествии
    /// </summary>
    [JsonObject("Report")]
    public class Report
    {
        /// <summary>
        /// ID происшествия
        /// </summary>
        [JsonProperty("ID")]
        [Key]
        public int ID { get; set; }

        /// <summary>
        /// Фото происшествия
        /// </summary>
        [JsonProperty("Photo")]
        [Required]
        public Byte[] Photo { get; set; }

        /// <summary>
        /// Наименование цеха
        /// </summary>
        [JsonProperty("Department")]
        [Required]
        public string Department { get; set; }

        /// <summary>
        /// Дата происшествия
        /// </summary>
        [JsonProperty("Date")]
        [Required]
        public DateTime Date { get; set; }

        /// <summary>
        /// Время происшествия
        /// </summary>
        [JsonProperty("Time")]
        [Required]
        public TimeSpan Time { get; set; }

        /// <summary>
        /// Описание происшествия
        /// </summary>
        [JsonProperty("Description")]
        [Required]
        public string Description { get; set; }

        /// <summary>
        /// Доклад о происшествии
        /// </summary>
        /// <param name="description">Описание происшествия</param>
        /// <param name="department">Наименование цеха</param>
        /// <param name="photo">Фото происшествия</param>
        /// <param name="date">Дата происшествия</param>
        /// <param name="time">Время происшествия</param>
        public Report(dynamic photo, dynamic department, dynamic date, dynamic time, dynamic description)
        {
            Photo = photo;
            Department = department;
            Date = date;
            Time = time;
            Description = description;
        }
        public Report() { }
    }
}