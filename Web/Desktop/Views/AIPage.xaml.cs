using System.Collections.Generic;
using System.Drawing;
using System;
using System.Windows.Controls;
using Yolov5Net.Scorer.Models;
using Yolov5Net.Scorer;
using Image = System.Drawing.Image;
namespace Desktop.Views
{
    public partial class AIPage : Page
    {
        public AIPage()
        {
            InitializeComponent();
            Foo();
        }
        void Foo()
        {
            string absPath = "C:/Users/Дмитрий/Desktop/Xacaton/holliwid/xacaton_2022/Web/Desktop/Views/";
            using var image = Image.FromFile($"{absPath}Assets/test.jpg");
            using var scorer = new YoloScorer<YoloCocoP5Model>($"{absPath}Assets/weights.pt");
            List<YoloPrediction> predictions = scorer.Predict(image);
            using var graphics = Graphics.FromImage(image);
            foreach (var prediction in predictions)
            {
                double score = Math.Round(prediction.Score, 2);
                graphics.DrawRectangles(new Pen(prediction.Label.Color, 1),
                    new[] { prediction.Rectangle });
                var (x, y) = (prediction.Rectangle.X - 3, prediction.Rectangle.Y - 23);
                graphics.DrawString($"{prediction.Label.Name} ({score})",
                    new Font("Arial", 16, GraphicsUnit.Pixel), new SolidBrush(prediction.Label.Color),
                    new PointF(x, y));
            }
            image.Save($"{absPath}Assets/result.jpg");
        }
    }
}