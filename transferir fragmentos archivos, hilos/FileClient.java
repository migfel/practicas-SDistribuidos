import java.io.*;
import java.net.*;

public class FileClient {
    public static void main(String[] args) {
        try {
            Socket socket = new Socket("localhost", 12345);
            DataOutputStream dos = new DataOutputStream(socket.getOutputStream());

            // Enviar nombre del archivo
            dos.writeUTF("example.bin");

            // Enviar archivo en 10 pedazos
            FileInputStream fis = new FileInputStream("path/to/example.bin");
            byte[] buffer = new byte[1024];
            int bytesRead;
            for (int i = 0; i < 10; i++) {
                bytesRead = fis.read(buffer);
                dos.write(buffer, 0, bytesRead);
            }

            System.out.println("File sent successfully.");

            fis.close();
            dos.close();
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
