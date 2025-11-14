import java.io.*;
import java.net.*;

public class FileServerPorcentaje {
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

            FileOutputStream fos = new FileOutputStream("received_" + fileName);
            byte[] buffer = new byte[8192]; // 8 KB
            long totalRead = 0;
            int bytesRead;
            int lastPercent = 0;

            System.out.println("Recibiendo archivo: " + fileName + " (" + fileSize + " bytes)");

            // 3. Leer exactamente fileSize bytes
            while (totalRead < fileSize && (bytesRead = dis.read(buffer)) != -1) {
                fos.write(buffer, 0, bytesRead);
                totalRead += bytesRead;

                int percent = (int) ((totalRead * 100) / fileSize);
                if (percent != lastPercent) {
                    System.out.print("\rProgreso recepción: " + percent + "%");
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
