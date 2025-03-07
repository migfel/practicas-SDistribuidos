import java.io.*;
import java.net.*;

public class ServidorConSkeleton {
    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(12345)) {
            System.out.println("Servidor esperando conexiones...");

            while (true) {
                // Aceptamos una conexión de cliente
                Socket socket = serverSocket.accept();
                System.out.println("Cliente conectado");

                // Creamos el skeleton para procesar la solicitud
                Skeleton skeleton = new Skeleton(socket);
                skeleton.procesar();  // Procesamos la solicitud

                // Cerramos la conexión
                //socket.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
