using System;
using System.ComponentModel.DataAnnotations;
using System.Windows.Controls;
namespace Desktop.Models
{
    /// <summary>
    /// Доклад о происшествии
    /// </summary>
    public class Report
    {
        /// <summary>
        /// ID происшествия
        /// </summary>
        [Key]
        public int ID { get; set; }

        /// <summary>
        /// Фото происшествия
        /// </summary>
        [Required]
        public Byte[] Photo { get; set; }

        /// <summary>
        /// Наименование цеха
        /// </summary>
        [Required]
        public string Department { get; set; }

        /// <summary>
        /// Время происшествия
        /// </summary>
        [Required]
        public int Time { get; set; }

        /// <summary>
        /// Описание происшествия
        /// </summary>
        [Required]
        public string Description { get; set; }

        /// <summary>
        /// Доклад о происшествии
        /// </summary>
        /// <param name="description">Описание происшествия</param>
        /// <param name="department">Наименование цеха</param>
        /// <param name="photo">Фото происшествия</param>
        /// <param name="time">Время происшествия</param>
        public Report(dynamic id, dynamic photo, dynamic department, dynamic time, dynamic description)
        {
            ID = id;
            Photo = photo;
            Department = department;
            Time = time;
            Description = description;
        }
        public Report() { }
    }
}