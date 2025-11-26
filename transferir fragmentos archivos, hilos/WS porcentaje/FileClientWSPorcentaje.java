import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;

public class FileClientWSPorcentaje {
    public static void main(String[] args) {
        try {
            // Archivo a enviar
            File file = new File("uno.mp4");
            long fileSize = file.length();

            if (!file.exists()) {
                System.out.println("El archivo no existe: " + file.getAbsolutePath());
                return;
            }

            URL url = new URL("http://localhost:8000/upload");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            // Configuración de la petición HTTP
            connection.setDoOutput(true);
            connection.setRequestMethod("POST");
            connection.setRequestProperty("X-File-Name", file.getName());
            connection.setRequestProperty("X-File-Size", String.valueOf(fileSize));
            connection.setFixedLengthStreamingMode(fileSize);
            connection.setRequestProperty("Content-Type", "application/octet-stream");

            System.out.println("Conectado al servidor HTTP. Enviando archivo: " + file.getName());
            System.out.println("Tamaño del archivo: " + fileSize + " bytes");

            byte[] buffer = new byte[64 * 1024]; // 64 KB

            long totalSent = 0;
            long lastPercent = -1;

            try (OutputStream os = connection.getOutputStream();
                 FileInputStream fis = new FileInputStream(file)) {

                int read;
                while ((read = fis.read(buffer)) != -1) {
                    os.write(buffer, 0, read);
                    totalSent += read;

                    long percent = (totalSent * 100) / fileSize;
                    if (percent != lastPercent) {
                        System.out.print("\rProgreso cliente: " + percent + "%");
                        lastPercent = percent;
                    }
                }

                os.flush();
            }

            System.out.println("\nEnvío completado. Esperando respuesta del servidor...");

            int responseCode = connection.getResponseCode();
            String responseMessage = connection.getResponseMessage();
            System.out.println("Código de respuesta: " + responseCode + " (" + responseMessage + ")");

            try (BufferedReader br = new BufferedReader(
                    new InputStreamReader(
                            responseCode >= 400 ? connection.getErrorStream() : connection.getInputStream()
                    ))) {

                String line;
                System.out.println("Respuesta del servidor:");
                while ((line = br.readLine()) != null) {
                    System.out.println(line);
                }
            }

            connection.disconnect();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
