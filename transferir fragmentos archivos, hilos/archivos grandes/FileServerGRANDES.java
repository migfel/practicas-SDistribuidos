import java.io.*;
import java.net.*;

public class FileServerGRANDES {
    public static void main(String[] args) {
        try {
            ServerSocket serverSocket = new ServerSocket(12345);
            System.out.println("Servidor listo...");

            while (true) {
                Socket client = serverSocket.accept();
                new Thread(new Handler(client)).start();
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

class Handler implements Runnable {
    private Socket socket;

    public Handler(Socket socket) {
        this.socket = socket;
    }

    public void run() {
        try {
            DataInputStream dis = new DataInputStream(socket.getInputStream());

            String fileName = dis.readUTF();
            long fileSize = dis.readLong(); // ⬅ recibe tamaño

            FileOutputStream fos = new FileOutputStream("received_" + fileName);
            byte[] buffer = new byte[4096];
            long totalRead = 0;
            int bytesRead;

            // ⬅ recibir exactamente fileSize bytes
            while (totalRead < fileSize &&
                   (bytesRead = dis.read(buffer)) != -1) {

                fos.write(buffer, 0, bytesRead);
                totalRead += bytesRead;
            }

            fos.close();
            dis.close();
            socket.close();

            System.out.println("Archivo " + fileName + " recibido correctamente.");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
