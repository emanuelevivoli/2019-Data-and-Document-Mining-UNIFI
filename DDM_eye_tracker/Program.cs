using System;
using Tobii.Interaction;
using Tobii.Interaction.Framework;

using System.IO;
using System.Diagnostics;

namespace DDM_test1
{
    class Program
    {
        private static Host _host;
        // private static GazePointDataStream _gazePointDataStream;
        private static FixationDataStream _fixationDataStream;
        private static DateTime _fixationBeginTime = default(DateTime);

        // 
        // CHANGE WITH YOURS THIS TWO PATHS
        //
        private static string path_base   = @"C:\Users\lello\Source\Repos\";           
        private static string python_path = @"C:\Users\lello\AppData\Local\Programs\Python\Python37\python.exe";  


        private static string stream_path   = path_base + @"DDM_eye_tracker\DDM_test1\Streams\";
        private static string path_to_py    = path_base + @"DDM_eye_tracker\DDM_test1\test_complete.py";


        public static void Main(string[] args)
        {
            // create host stream for Tobii
            _host = new Host();

            // _gazePointDataStream = _host.Streams.CreateGazePointDataStream();
            _fixationDataStream = _host.Streams.CreateFixationDataStream();
            
            // set params to save streams on file
            string gaze_path = "gazeStream.csv";
            string fixs_path = "fixationStream.csv";


            // call for save on file function
            stream_read_write(path_to_py, gaze_path, fixs_path);


            Console.Write("----------------------------------------------------------------------------------------------------");
            Console.ReadKey();
            
        }

        


        private static void stream_read_write(string path_to_py, string gaze_path, string fixs_path)
        {
            ProcessStartInfo start = new ProcessStartInfo();

            start.FileName = python_path; 
            start.Arguments = string.Format("{0}", path_to_py);
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            start.RedirectStandardInput = true;
            start.CreateNoWindow = true;

            int count = 0;
            bool flag = true;

            using (Process process = Process.Start(start))
            using (StreamWriter writer = process.StandardInput)
            using (StreamReader reader = process.StandardOutput)
            {
                // string all_paths = stream_path + count.ToString() + gaze_path + " " + stream_path + count.ToString() + fixs_path;
                string all_paths = stream_path + fixs_path;
                writer.WriteLine(all_paths);
                
                // StreamWriter gaze_outputFile = new StreamWriter(stream_path + count.ToString() + gaze_path);
                // StreamWriter fixation_outputFile = new StreamWriter(stream_path + count.ToString() + fixs_path);

                StreamWriter fixation_outputFile = new StreamWriter(all_paths);

                stream_on_file(fixation_outputFile); //gaze_outputFile);

                Console.WriteLine("written: " + all_paths);

                while (flag)
                {
                    string result = null;

                    while (result == null || result.Length == 0)
                    { result = reader.ReadLine(); }

                    if (result.Contains("END"))
                    {
                        flag = false;
                        Console.WriteLine("receive: " + result + "\n"); 
                    }
                    else
                    {
                        count = Int32.Parse(System.Text.RegularExpressions.Regex.Match(result, @"\d+").Value);
                        Console.WriteLine("photo name: " + result + "\n");
                    }
                    fixation_outputFile.WriteLine(result + ",-,-,-");
                    
                    // ToggleFixationDataStream();
                    // gaze_outputFile.Close();
                    

                    // Console.WriteLine("viewing: " + result + "\n");

                }
                fixation_outputFile.Close();
            }
        }

        private static void stream_on_file(StreamWriter fixation_outputFile) //, StreamWriter gaze_outputFile
        {
            // StreamWriter gaze_outputFile = new StreamWriter(Path.Combine(stream_path, gaze_path));
            // StreamWriter fixation_outputFile = new StreamWriter(Path.Combine(stream_path, fixs_path));

            /* 
            
            _gazePointDataStream.GazePoint((x, y, ts) =>
            {
                // Console.WriteLine("Timestamp: {0}\tX:{1}, Y:{2}", ts, x, y);
                gaze_outputFile.WriteLine("TS:{0},X:{1},Y:{2}", ts, x, y);
                Console.WriteLine("TS:{0},X:{1},Y:{2}", ts, x, y);
            }); 
            
             */

            _fixationDataStream
            .Begin((x, y, _) =>
            {
                        // Console.WriteLine("\n" + "Fixation started at X: {0}, Y: {1}", x, y);
                fixation_outputFile.WriteLine("FS,{0},{1},-", x, y);
                // Console.WriteLine("FS,{0},{1},-", x, y);
                _fixationBeginTime = DateTime.Now;
            })
            .Data((x, y, _) =>
            {
                        // Console.WriteLine("During fixation, currently at: X: {0}, Y: {1}", x, y);
                fixation_outputFile.WriteLine("DF,{0},{1},-", x, y);
                // Console.WriteLine("DF,{0},{1},-", x, y);
            })
            .End((x, y, _) =>
            {
                fixation_outputFile.WriteLine("FE,{0},{1},-", x, y);
                // Console.WriteLine("FE,{0},{1},-", x, y);
                if (_fixationBeginTime != default(DateTime))
                {
                            // Console.WriteLine("Fixation duration: {0}", DateTime.Now - _fixationBeginTime);
                    fixation_outputFile.WriteLine("TIME,-,-,{0}", DateTime.Now - _fixationBeginTime);
                    // Console.WriteLine("TIME,-,-,{0}", DateTime.Now - _fixationBeginTime);
                }
            });

        }

        /*        
        private static void ToggleGazePointDataStream()
        {
            if (_gazePointDataStream != null)
            _gazePointDataStream.IsEnabled = !_gazePointDataStream.IsEnabled;
        }
        */
        private static void ToggleFixationDataStream()
        {
            if (_fixationDataStream != null)
            _fixationDataStream.IsEnabled = !_fixationDataStream.IsEnabled;
        }
        
        /*
        private static void ToggleStream()
        {
            if (_gazePointDataStream != null)
            _gazePointDataStream.IsEnabled = !_gazePointDataStream.IsEnabled;

            if (_fixationDataStream != null)
            _fixationDataStream.IsEnabled = !_fixationDataStream.IsEnabled;
        }
        */

    }
    
}
