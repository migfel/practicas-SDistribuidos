import java.io.*;
import java.net.*;

public class FileClientGRANDES {
    public static void main(String[] args) {
        try {
            Socket socket = new Socket("localhost", 12345);
            DataOutputStream dos = new DataOutputStream(socket.getOutputStream());

            File file = new File("uno.mp4");
            long fileSize = file.length();

            // 1. Enviar nombre
            dos.writeUTF(file.getName());

            // 2. Enviar tamaño del archivo
            dos.writeLong(fileSize);

            // 3. Enviar contenido
            FileInputStream fis = new FileInputStream(file);
            byte[] buffer = new byte[4096];
            int bytesRead;

            while ((bytesRead = fis.read(buffer)) != -1) {
                dos.write(buffer, 0, bytesRead);
            }

            fis.close();
            dos.close();
            socket.close();

            System.out.println("Archivo enviado correctamente.");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
