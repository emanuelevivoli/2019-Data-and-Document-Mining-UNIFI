using System;
using System.Collections.Generic;
using Tobii.Interaction;
using Tobii.StreamEngine;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace ClientCs_ServerPy
{
    class Client_vFRA
    {
        private static Host _host;
        private static FixationDataStream _fixationDataStream;
        private static DateTime _fixationBeginTime = default(DateTime);
        private static byte[] bytesToSend;
        private static string app;
        private static bool flag = true;

        static void Main(string[] args)
        {
            _host = new Host();
            _fixationDataStream = _host.Streams.CreateFixationDataStream();

            Console.WriteLine("create tcp socket");
            TcpClient tcp = new TcpClient("localhost", 12345);
            
            
                NetworkStream nwStream = tcp.GetStream();
                nwStream.Flush();

                _fixationDataStream
                .Begin((x, y, _) =>
                {
                    
                    Console.WriteLine("FS,{0},{1},-", x, y);
                    string fin_x = x.ToString().Replace(",", ".");
                    string fin_y = y.ToString().Replace(",", ".");
                    app = "FS," + fin_x + "," + fin_y+",-";

                    //Console.WriteLine("B");
                    //app = "B";
                    bytesToSend = ASCIIEncoding.ASCII.GetBytes(app.ToCharArray());
                    nwStream.Write(bytesToSend, 0, bytesToSend.Length);
                    
                    _fixationBeginTime = DateTime.Now;
                })
                .Data((x, y, _) =>
                {

                    Console.WriteLine("DF,{0},{1},-", x, y);
                    string fin_x = x.ToString().Replace(",", ".");
                    string fin_y = y.ToString().Replace(",", ".");
                    app = "DF," + fin_x + "," + fin_y + ",-";

                    //Console.WriteLine("D");
                    //app = "D";
                    bytesToSend = ASCIIEncoding.ASCII.GetBytes(app.ToCharArray());
                    nwStream.Write(bytesToSend, 0, bytesToSend.Length);
                })
                .End((x, y, _) =>
                {
                    
                    Console.WriteLine("FE,{0},{1},-", x, y);
                    string fin_x = x.ToString().Replace(",", ".");
                    string fin_y = y.ToString().Replace(",", ".");
                    app = "FE," + fin_x + "," + fin_y+",-";
                    //Console.WriteLine("E");
                    //app = "E";

                    bytesToSend = ASCIIEncoding.ASCII.GetBytes(app.ToCharArray());
                    nwStream.Write(bytesToSend, 0, bytesToSend.Length);

                    if (_fixationBeginTime != default(DateTime))
                    {
                        Console.WriteLine("TIME,-,-,{0}", DateTime.Now - _fixationBeginTime);
                        app = "TIME,-,-," + (DateTime.Now - _fixationBeginTime).ToString();
                        //Console.WriteLine("T");
                        //app = "T";

                        bytesToSend = ASCIIEncoding.ASCII.GetBytes(app.ToCharArray());
                        nwStream.Write(bytesToSend, 0, bytesToSend.Length);
                    }

                    //flag = false;
                });


            Console.ReadKey();

            tcp.Close();
            Console.WriteLine("close socket");
        }
    }
}
