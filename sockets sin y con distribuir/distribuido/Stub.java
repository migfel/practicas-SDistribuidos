import java.io.*;
import java.net.*;

public class Stub implements ServicioOperaciones {
    private Socket socket;
    private DataInputStream input;
    private DataOutputStream output;

    public Stub(String host, int port) throws IOException {
        this.socket = new Socket(host, port);
        this.input = new DataInputStream(socket.getInputStream());
        this.output = new DataOutputStream(socket.getOutputStream());
    }

    @Override
    public int sumar(int a, int b) throws IOException {
        output.writeUTF("sumar");
        output.writeInt(a);
        output.writeInt(b);
        return input.readInt();
    }

    @Override
    public int restar(int a, int b) throws IOException {
        output.writeUTF("restar");
        output.writeInt(a);
        output.writeInt(b);
        return input.readInt();
    }

    public void cerrar() throws IOException {
        socket.close();
    }
}
