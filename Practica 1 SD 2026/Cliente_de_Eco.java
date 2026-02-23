

import java.io.*;
import java.net.*;

public class Cliente_de_Eco {
    public static void main(String[] args) throws IOException {
        
        if (args.length != 2) {
            System.err.println(
                "Uso desde consola: java Cliente_de_Eco <nombre de host (computadora)> <numero puerto>");
            System.exit(1);
        }

        String nombreHost = args[0];
        int numeroPuerto = Integer.parseInt(args[1]);

        try (
            Socket socketEco = new Socket(nombreHost, numeroPuerto);
            PrintWriter escritor = new PrintWriter(socketEco.getOutputStream(), true);
            
            BufferedReader lector = new BufferedReader(new InputStreamReader(socketEco.getInputStream()));
            BufferedReader teclado = new BufferedReader( new InputStreamReader(System.in))
        ) {
            String usuarioEscribio;
            while ((usuarioEscribio = teclado.readLine()) != null) {
               //escritor.println(usuarioEscribio);
               System.out.println("El eco del servidor dice:  " + teclado.readLine());
            }
        } catch (UnknownHostException e) {
            System.err.println("No conozco al host " + nombreHost);
            System.exit(1);
        } catch (IOException e) {
            System.err.println("no se pudo obtener E/S para la conexion " +
                nombreHost);
            System.exit(1);
        } 
    }
}
