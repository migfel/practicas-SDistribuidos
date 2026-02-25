import java.io.*;
import java.net.*;

public class ClienteTocToc {
    public static void main(String[] args) throws IOException {
        // declaramos un socket para recibir y enviar datos
        Socket TocTocSocket = null;
        //declaramos un escritor para escribir los datos que se enviaran en el socket
        PrintWriter EscritorEnSocket = null;
        // declaramos un lector de flujo de texto (el flujo es una secuencia de entrada de caracteres, 
        //almacenando caracteres en un buffer para proporcionar una lectura eficiente 
        //de caracteres, líneas y matrices.
        BufferedReader LectorDeSocket = null;

        try {
            //abrimos el socket TocTocSocket para hacer peticiones al servidor
            TocTocSocket = new Socket("127.0.0.1", 4444);
            System.out.println("Estamos listos en el puerto " + 4444);
            //asignamos a lector y escritor el flujo de datos del socket
            EscritorEnSocket = new PrintWriter(TocTocSocket.getOutputStream(), true);
            LectorDeSocket = new BufferedReader(new InputStreamReader(TocTocSocket.getInputStream()));
        } catch (UnknownHostException e) {
            System.err.println("No se conoce al anfitrión: Juanito.");
            System.exit(1);
        } catch (IOException e) {
            System.err.println("No se pudo obtener E / S para la conexión a: Juanito.");
            System.exit(1);
        }
// abrimos un lector , para leer el texto desde consola 
        BufferedReader EntradaTeclado = new BufferedReader(new InputStreamReader(System.in));
        //declaramos cadenas para almacenar el texto recibido del servidor 
        //y otra para el texto recibido desde consola por el usuario
        String DelServidor;
        String DelUsuario;
// leemos lo que dice el servidor , y si hay algo escrito procedemos a ingresar al ciclo while
        while ((DelServidor = LectorDeSocket.readLine()) != null) {
            System.out.println("El Servidor dice: " + DelServidor);
           // si el usuario escribe Adios, significa que hay que cerrar la transmision de datos
            if (DelServidor.equals("Adios."))
                break;
// leeemos desde la consola del usuario
            DelUsuario = EntradaTeclado.readLine();
            // si si leimos algo ( quiere decir que el usuario escribio algo) 
	    if (DelUsuario != null) {
                System.out.println("El Cliente dice: " + DelUsuario);
                EscritorEnSocket.println(DelUsuario);
	    }
        }

        EscritorEnSocket.close();
        LectorDeSocket.close();
        EntradaTeclado.close();
        TocTocSocket.close();
    }
}
