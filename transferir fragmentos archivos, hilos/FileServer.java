import java.io.*;
import java.net.*;

public class FileServer {

    public static void main(String[] args) {
        try {
            // Servidor escuchando en el puerto 12345
            ServerSocket serverSocket = new ServerSocket(12345);
            System.out.println("FileServer escuchando en el puerto 12345...");

            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Cliente conectado: " + clientSocket.getInetAddress());

                // Hilo para atender a cada cliente
                Thread clientThread = new Thread(new ClientHandler(clientSocket));
                clientThread.start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

class ClientHandler implements Runnable {
    private Socket clientSocket;

    public ClientHandler(Socket clientSocket) {
        this.clientSocket = clientSocket;
    }

    @Override
    public void run() {
        try {
            DataInputStream dis =
                    new DataInputStream(clientSocket.getInputStream());

            // Leer nombre del archivo
            String fileName = dis.readUTF();
            System.out.println("Receiving file: " + fileName);

            // Crear un nuevo archivo (prefijo "received_")
            File file = new File("received_" + fileName);
            FileOutputStream fos = new FileOutputStream(file);

            // Recibir el archivo en fragmentos
            byte[] buffer = new byte[1024];
            int bytesRead;

            // Leer hasta que el cliente cierre el stream (read() = -1)
            while ((bytesRead = dis.read(buffer)) != -1) {
                fos.write(buffer, 0, bytesRead);
            }

            System.out.println("File received successfully.");

            fos.close();
            dis.close();
            clientSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
