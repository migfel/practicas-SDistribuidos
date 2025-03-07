import java.io.*;
import java.net.*;

public class ServidorSinSkeleton {
    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(12345)) {
            System.out.println("Servidor esperando conexiones...");

            while (true) {
                // Aceptamos una conexión de cliente
                Socket socket = serverSocket.accept();
                System.out.println("Cliente conectado");

                // Creamos los flujos de entrada y salida para la comunicación
                DataInputStream input = new DataInputStream(socket.getInputStream());
                DataOutputStream output = new DataOutputStream(socket.getOutputStream());

                // Leemos la operación que el cliente quiere realizar (sumar o restar)
                String operacion = input.readUTF();
                int num1 = input.readInt();
                int num2 = input.readInt();

                // Ejecutamos la operación
                int resultado = 0;
                if (operacion.equals("sumar")) {
                    resultado = sumar(num1, num2);
                } else if (operacion.equals("restar")) {
                    resultado = restar(num1, num2);
                }

                // Enviamos el resultado al cliente
                output.writeInt(resultado);

                // Cerramos la conexión
                socket.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Método para sumar
    public static int sumar(int a, int b) {
        return a + b;
    }

    // Método para restar
    public static int restar(int a, int b) {
        return a - b;
    }
}
