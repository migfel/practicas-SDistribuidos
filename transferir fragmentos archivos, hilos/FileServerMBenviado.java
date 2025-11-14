import java.io.*;
import java.net.*;

public class FileServerMBenviado {
    public static void main(String[] args) {
        try {
            ServerSocket serverSocket = new ServerSocket(12345);
            System.out.println("Servidor listo en puerto 12345...");

            while (true) {
                Socket client = serverSocket.accept();
                System.out.println("Cliente conectado: " + client.getInetAddress());
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

            // 1. Leer nombre del archivo
            String fileName = dis.readUTF();

            // 2. Leer tamaño del archivo
            long fileSize = dis.readLong();
            double fileSizeMB = fileSize / (1024.0 * 1024.0);

            FileOutputStream fos = new FileOutputStream("received_" + fileName);
            byte[] buffer = new byte[8192]; // 8 KB
            long totalRead = 0;
            int bytesRead;
            int lastPercent = -1;

            System.out.printf("Recibiendo archivo: %s (%.2f MB)%n", fileName, fileSizeMB);

            // 3. Leer exactamente fileSize bytes
            while (totalRead < fileSize && (bytesRead = dis.read(buffer)) != -1) {
                fos.write(buffer, 0, bytesRead);
                totalRead += bytesRead;

                int percent = (int) ((totalRead * 100) / fileSize);
                double readMB = totalRead / (1024.0 * 1024.0);

                if (percent != lastPercent) {
                    System.out.printf(
                        "\rProgreso recepción: %3d%% (%.2f / %.2f MB)",
                        percent, readMB, fileSizeMB
                    );
                    lastPercent = percent;
                }
            }

            System.out.println("\nRecepción completada de: " + fileName);

            fos.close();
            dis.close();
            socket.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
