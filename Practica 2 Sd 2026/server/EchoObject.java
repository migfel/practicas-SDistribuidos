
package server;
import java.net.*;
import java.io.*;
import java.text.*;
import java.util.*;
import rmi.EchoInt;
public class EchoObject implements EchoInt {
    String myURL="localhost";
    //Constructor de la clase EchoObject
    public EchoObject(){
        try {
// obtengo el nombre del equipo donde estoy ejecutando y lo guardo en la propiedad MyURL
            myURL=InetAddress.getLocalHost().getHostName();
        } catch (UnknownHostException e) 
        {
     // si no pude conocer el nombre del equipo, mantengo el nombre localhost para MyURL
            myURL="localhost";
        }
    }
// el Metodo Echo que es la implementacion de la interfaz EchoInt
    public String echo(String input) throws java.rmi.RemoteException {
        Date h = new Date();
        // obtengo la fechay hora actual 
        String fecha = DateFormat.getTimeInstance(3,Locale.FRANCE).format(h);
        String ret = myURL + ":" + fecha + "> " + input;
        System.out.println("Procesando: '" + input + "'");
        try {
            Thread.sleep(3000); ret = ret + " (retrasada 3 segundos)";
        } catch (InterruptedException e) {}
        System.out.println("Procesamiento de '"+ input +"'terminado.");
        return ret;
    }
}
