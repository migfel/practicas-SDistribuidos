import java.io.*;
import java.net.*;

public class ClienteSinStub {
    public static void main(String[] args) {
        try (Socket socket = new Socket("localhost", 12345)) {
            // Creamos los flujos de entrada y salida
            DataInputStream input = new DataInputStream(socket.getInputStream());
            DataOutputStream output = new DataOutputStream(socket.getOutputStream());

            // Enviamos la operación que queremos realizar (sumar o restar)
            output.writeUTF("sumar");  // O "restar"
            output.writeInt(5);
            output.writeInt(3);

            // Recibimos el resultado del servidor
            int resultado = input.readInt();
            System.out.println("Resultado: " + resultado);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
