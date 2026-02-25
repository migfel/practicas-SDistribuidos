import java.net.*;
import java.io.*;

public class ServidorTocToc {
    public static void main(String[] args) throws IOException {

        //Se declara un ServerSocket para recibir conexiones
        //este socket nunca transmitira datos  (
        ServerSocket serverSocket = null;
        try {
           // el socket se abre en el puerto 4444
            serverSocket = new ServerSocket(4444);
        } catch (IOException e) {
            System.err.println("No puedo escuchar en el puerto: 4444.");
            System.exit(1); // cerrar y avisar al sistema operativo que terminamos con estatus de 0
        }

        //el servidor declara que  usara un Socket para transmitir datos
        Socket clientSocket = null;
        try {
        // el socket acepta la peticion de conexion
            clientSocket = serverSocket.accept();
        } catch (IOException e) {
            System.err.println("Fallo al aceptar la peticion.");
            System.exit(1);
        }
// abrimos escritores y lectores para leer desde el socket 
        PrintWriter EscritorSalida = new PrintWriter(clientSocket.getOutputStream(), true);
        BufferedReader LectorEntrada = new BufferedReader(
				new InputStreamReader(
				clientSocket.getInputStream()));
        //declaramos dos variables que sirven para almacenar temporalmente lo que se lee 
        //y escribe en el socket , es una variable de paso o de buffer
        String LineaDeEntrada, LineaDeSalida;
        //creamos el objeto Protocolo para poder procesar los mensajes que son validos 
        //en el intercambio de mensajes
        ProtocoloTocToc ptt = new ProtocoloTocToc();
// le pedimos a la clase protocolo que procese un mensaje, 
        // en este caso es un  nulo , y recibimos la respuesta de Protocolo en una cadena de texto
        LineaDeSalida = ptt.processInput(null);
        //imprimimos en el escritor el contenido de la variable LineaSalida (respuesta del Protocolo)
        EscritorSalida.println(LineaDeSalida);
//leemos desde el socket  y si es diferente de null, entonces hay texto recibido 

        while ((LineaDeEntrada = LectorEntrada.readLine()) != null) {
          
        // Se procede a enviar ese texto recibido a Protocolo 
    //para que nos indique que debemos responder y la respuesta la guardamos en LineaDeSalida
             LineaDeSalida = ptt.processInput(LineaDeEntrada);
             //escribimos la respuesta en el escritor del Socket
             EscritorSalida.println(LineaDeSalida);
             //ahora ya que lo escribimos verificamos si es un Adios y procedemos a cerrar todo
             if (LineaDeSalida.equals("Adios."))
                break;
        }
        //liberamos memoria
        EscritorSalida.close();
        LectorEntrada.close();
        clientSocket.close();
        serverSocket.close();
    }
}
