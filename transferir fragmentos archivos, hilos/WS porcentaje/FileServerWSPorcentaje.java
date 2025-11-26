import java.io.*;
import java.net.InetSocketAddress;

import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

public class FileServerWSPorcentaje {

    public static void main(String[] args) {
        try {
            int port = 8000;
            HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
            System.out.println("Servidor HTTP listo en puerto " + port + "...");
            server.createContext("/upload", new FileUploadHandler());
            server.setExecutor(null); // usa el executor por defecto
            server.start();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    static class FileUploadHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                String msg = "Método no permitido. Usa POST.";
                exchange.sendResponseHeaders(405, msg.getBytes().length);
                OutputStream os = exchange.getResponseBody();
                os.write(msg.getBytes());
                os.close();
                return;
            }

            Headers headers = exchange.getRequestHeaders();
            String fileName = headers.getFirst("X-File-Name");
            String fileSizeHeader = headers.getFirst("X-File-Size");
            long fileSize = -1;

            if (fileName == null || fileName.isEmpty()) {
                fileName = "archivo_recibido.bin";
            }

            try {
                if (fileSizeHeader != null) {
                    fileSize = Long.parseLong(fileSizeHeader);
                }
            } catch (NumberFormatException e) {
                fileSize = -1;
            }

            System.out.println("Recibiendo archivo: " + fileName);
            if (fileSize > 0) {
                System.out.println("Tamaño reportado: " + fileSize + " bytes");
            }

            File outputFile = new File("recibido_" + fileName);
            long totalRead = 0;
            byte[] buffer = new byte[64 * 1024]; // 64 KB

            try (InputStream is = exchange.getRequestBody();
                 FileOutputStream fos = new FileOutputStream(outputFile)) {

                int read;
                long lastPercent = -1;

                while ((read = is.read(buffer)) != -1) {
                    fos.write(buffer, 0, read);
                    totalRead += read;

                    if (fileSize > 0) {
                        long percent = (totalRead * 100) / fileSize;
                        if (percent != lastPercent) {
                            System.out.print("\rProgreso servidor: " + percent + "%");
                            lastPercent = percent;
                        }
                    }
                }

                System.out.println("\nRecepción completada de: " + outputFile.getAbsolutePath());

            } catch (Exception e) {
                e.printStackTrace();
            }

            String response = "Archivo recibido correctamente en el servidor.";
            exchange.sendResponseHeaders(200, response.getBytes().length);
            OutputStream os = exchange.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }
    }
}
