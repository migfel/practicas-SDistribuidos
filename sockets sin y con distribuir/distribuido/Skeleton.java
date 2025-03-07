import java.io.*;
import java.net.*;

public class Skeleton implements ServicioOperaciones {
    private Socket socket;
    private DataInputStream input;
    private DataOutputStream output;

    public Skeleton(Socket socket) throws IOException {
        this.socket = socket;
        this.input = new DataInputStream(socket.getInputStream());
        this.output = new DataOutputStream(socket.getOutputStream());
    }

    public int sumar(int a, int b) {
        return a + b;
    }

    public int restar(int a, int b) {
        return a - b;
    }

    // Método para procesar la solicitud del cliente
    public void procesar() throws IOException {
        String operacion = input.readUTF();
        int num1 = input.readInt();
        int num2 = input.readInt();

        int resultado = 0;
        if (operacion.equals("sumar")) {
            resultado = sumar(num1, num2);
        } else if (operacion.equals("restar")) {
            resultado = restar(num1, num2);
        }

        // Enviamos el resultado al cliente
        output.writeInt(resultado);
    }
}

