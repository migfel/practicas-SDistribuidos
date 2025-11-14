import java.io.*;
import java.net.*;

public class FileClient {
    public static void main(String[] args) {
        try {
            Socket socket = new Socket("localhost", 12345);
            DataOutputStream dos = new DataOutputStream(socket.getOutputStream());

            // Enviar nombre del archivo
            dos.writeUTF("uno.mp4");

            // Enviar archivo en fragmentos
            FileInputStream fis = new FileInputStream("uno.mp4");
            byte[] buffer = new byte[1024];
            int bytesRead;

            // Leer hasta que read() regrese -1 (fin del archivo)
            while ((bytesRead = fis.read(buffer)) != -1) {
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
