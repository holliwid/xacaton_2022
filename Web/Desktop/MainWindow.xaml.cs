using System.Windows;
using System.Net.Http;
using System.IO;
using Newtonsoft.Json;
using System.Net;
using System.Text;
using System.Data.Common;

namespace Desktop
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }
        private async void button_Click(object sender, RoutedEventArgs e)
        {
            #region Запрос данных из БД
            using (HttpClient client = new())
            {
                var response = await client.GetAsync($"https://localhost:7237/Report/Get/{1}");
                response.EnsureSuccessStatusCode();
                if (response.IsSuccessStatusCode)
                {
                    var stream = await response.Content.ReadAsStreamAsync();
                    using (var streamReader = new StreamReader(stream))
                    {
                        using (var jsonTextReader = new JsonTextReader(streamReader))
                        {
                            var jsonSerializer = new JsonSerializer();
                            object data = jsonSerializer.Deserialize(jsonTextReader) ?? "No data found";
                            Output.Text = $"{data}";
                        }
                    }
                }
                else
                {
                    Output.Text = $"Server error code {response.StatusCode}";
                }
            }
            #endregion

            #region Добавление данных в бд

            #endregion
        }
    }
}