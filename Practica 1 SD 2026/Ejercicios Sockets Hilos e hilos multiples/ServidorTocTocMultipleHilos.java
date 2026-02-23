import java.net.*;
import java.io.*;

public class ServidorTocTocMultipleHilos extends Thread {
    private Socket socket = null;

    public ServidorTocTocMultipleHilos(Socket socketenviada) {
	//ejecuta el contructor de la clase Thread ( con esto hace propio
	 //todo el codigo de la clase Thread)
	super("ServidorTocTocMultipleHilos");
	//ahora le decimos al objeto socket de esta clase ServidorTocTocMultiplesHilos
	//que va a tener todos los valores recibidos en la variable socketenviada 
	// que es la que envio el ServidorTocTocMultiple 
	this.socket = socketenviada;
    }

// este metodo es el equivalente al main, ( estamos en un hilo por eso no hay main)
    //es un metodo que cada hilo lo ejecutara de forma independiente
    // puede haber muchos hilos , por supuesto
    public void run() {

	try {
		//abrimos el escritor del Socket 
	    PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
	    //abirmos el lector del socket
	    BufferedReader in = new BufferedReader(
				    new InputStreamReader(
				    socket.getInputStream()));
//declaramos variables de paso para almacenar temporalmente, cada linea de
// lo que se escribe y lee desde el socket
	    String LineaDeEntrada, LineaDeSalida;
	    //creamos el objeto del protocolo para poder procesar el texto  de mensajes enviados
	    ProtocoloTocToc ptt = new ProtocoloTocToc();
	   // procesamos
	    LineaDeSalida = ptt.processInput(null);
	    out.println(LineaDeSalida);

	    while ((LineaDeEntrada = in.readLine()) != null) {
		LineaDeSalida = ptt.processInput(LineaDeEntrada);
		out.println(LineaDeSalida);
		if (LineaDeSalida.equals("Adios"))
		    break;
	    }
	    out.close();
	    in.close();
	    socket.close();

	} catch (IOException e) {
	    e.printStackTrace();
	}
    }
}
