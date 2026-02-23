

import java.net.*; // paquete que contienen clases de red , todo lo necesario para comunicarme en red
import java.io.*; // paquete que contienen clases para E/S teclado y monitor

public class Servidor_Eco {
    
    public static void main(String[] args) throws IOException {
        
        if (args.length != 1) {
            System.err.println("Uso desde consola:  <numero puerto>");

            System.exit(1);
        }
        
        int numeroPuerto = Integer.parseInt(args[0]);// convertimos el numero de puerto
        
        try (
            ServerSocket socketdelServidor =
                new ServerSocket(Integer.parseInt(args[0]));//escuchando peticiones
            Socket socketdelCliente = socketdelServidor.accept();// se acepta la peticion     
            PrintWriter escritor =
                new PrintWriter(socketdelCliente.getOutputStream(), true);                   
            BufferedReader lector = new BufferedReader(
                new InputStreamReader(socketdelCliente.getInputStream()));
        ) {
            String linealeida;
            while ((linealeida = lector.readLine()) != null) {
                escritor.println(linealeida);
            }
        } catch (IOException e) {
            System.out.println(" ocurrio una excepcion cuando intentamos escuchar "
                + numeroPuerto + " o esperando por una conexicon");
            System.out.println(e.getMessage());
        }
    }
}
