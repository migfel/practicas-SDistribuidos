import java.net.*;
import java.io.*;

public class ProtocoloTocToc {
    private static final int ESPERANDO = 0;
    private static final int ENVIATOCTOC = 1;
    private static final int PISTAENVIADA = 2;
    private static final int OTRA = 3;

    private static final int NUMEROBROMAS = 5;

    private int estado = ESPERANDO;
    private int BromaActual = 0;

    private String[] pistas = { "Juanito", "Pequeña anciana", "Caray", "Quien", "Quien" };
    private String[] respuestas = { "Juanito enciende la calefaccion, hace frio aqui!",
                                 "Yo no sabia que podias cantar !",
                                 "Salud!",
                                 "¿Aqui hay una lechuza?",
                                 "¿Aqui hay Eco?" };

    public String processInput(String TextoRecibido) {
        String textoDeSalida = null;

        if (estado == ESPERANDO) {
            textoDeSalida = "Toc! Toc!";
            estado = ENVIATOCTOC;
        } else if (estado == ENVIATOCTOC) {
            if (TextoRecibido.equalsIgnoreCase("¿Quién está ahí?")) {
                textoDeSalida = pistas[BromaActual];
                estado = PISTAENVIADA;
            } else {
                textoDeSalida = "Se supone que debes decir  \"¿Quién está ahí?\"! " +
			    "Intenta de nuevo . Toc! Toc!";
            }
        } else if (estado == PISTAENVIADA) {
            if (TextoRecibido.equalsIgnoreCase(pistas[BromaActual] + "¿Quien?")) {
                textoDeSalida = respuestas[BromaActual] + "¿Quieres otro? (y/n)";
                estado = OTRA;
            } else {
                textoDeSalida = "Se supone que debes decir \"" + 
			    pistas[BromaActual] + 
			    " Quien?\"" + 
			    "!Intenta de nuevo . Toc! Toc!";
                estado = ENVIATOCTOC;
            }
        } else if (estado == OTRA) {
            if (TextoRecibido.equalsIgnoreCase("y")) {
                textoDeSalida = "Toc! Toc!";
                if (BromaActual == (NUMEROBROMAS - 1))
                    BromaActual = 0;
                else
                    BromaActual++;
                estado = ENVIATOCTOC;
            } else {
                textoDeSalida = "Adios.";
                estado = ESPERANDO;
            }
        }
        return textoDeSalida;
    }
}
