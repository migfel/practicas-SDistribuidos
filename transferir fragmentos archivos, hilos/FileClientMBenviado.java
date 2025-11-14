import java.io.*;
import java.net.*;

public class FileClientMBenviado {
    public static void main(String[] args) {
        try {
            // Archivo a enviar
            File file = new File("uno.mp4");
            long fileSize = file.length();

            if (!file.exists()) {
                System.out.println("El archivo no existe: " + file.getAbsolutePath());
                return;
            }

            Socket socket = new Socket("localhost", 12345);
            DataOutputStream dos = new DataOutputStream(socket.getOutputStream());

            // 1. Enviar nombre del archivo
            dos.writeUTF(file.getName());

            // 2. Enviar tamaño del archivo
            dos.writeLong(fileSize);

            // 3. Enviar contenido del archivo
            FileInputStream fis = new FileInputStream(file);
            byte[] buffer = new byte[8192]; // 8 KB
            int bytesRead;
            long totalSent = 0;
            int lastPercent = -1;

            double fileSizeMB = fileSize / (1024.0 * 1024.0);

            System.out.printf("Enviando archivo: %s (%.2f MB)%n", file.getName(), fileSizeMB);

            while ((bytesRead = fis.read(buffer)) != -1) {
                dos.write(buffer, 0, bytesRead);
                totalSent += bytesRead;

                int percent = (int) ((totalSent * 100) / fileSize);
                double sentMB = totalSent / (1024.0 * 1024.0);

                // Solo actualizamos cuando cambie el porcentaje para no saturar la consola
                if (percent != lastPercent) {
                    System.out.printf(
                        "\rProgreso envío: %3d%% (%.2f / %.2f MB)",
                        percent, sentMB, fileSizeMB
                    );
                    lastPercent = percent;
                }
            }

            System.out.println("\nEnvío completado.");

            fis.close();
            dos.close();
            socket.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
