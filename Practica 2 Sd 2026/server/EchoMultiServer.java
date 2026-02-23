/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package server;
import java.net.*;
import java.io.*;
public class EchoMultiServer {
    private static ServerSocket serverSocket = null;
    public static void main(String[] args) throws IOException {
        try {
            serverSocket = new ServerSocket(7);
        } catch (IOException e) {
            System.out.println("EchoMultiServer: could not listen on port: 7, " + e.toString());
            System.exit(1);
        }
        System.out.println("EchoMultiServer listening on port: 7");
        boolean listening = true;
        Socket clientSocket = null;
        while (listening) {
        //EJERCICIO: aceptar una nueva conexión
        //EJERCICIO: y crear un Thread para que la gestione
            /*Runnable Cliente;
            Cliente = new EchoMultiServerThread(serverSocket.accept());
            Thread hilo=new Thread(Cliente);
            hilo.start();*/
            clientSocket = serverSocket.accept();
            Runnable Cliente =new EchoMultiServerThread(clientSocket);
            Thread hilo=new Thread(Cliente);
            hilo.start();
        }
        try {
            serverSocket.close();
        } catch (IOException e) {
            System.err.println("Could not close server socket." +
            e.getMessage());
        }
    }
}
