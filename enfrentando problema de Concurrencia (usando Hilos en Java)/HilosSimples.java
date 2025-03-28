

public class HilosSimples {

    // Despliega un mensaje precedido del hilo actual 
    static void mensajeHilo(String mensaje) {
        String threadName =
            Thread.currentThread().getName();
        System.out.format("%s: %s%n",
                          threadName,
                          mensaje);
    }

    private static class ciclomensajes
        implements Runnable {
        public void run() {
            String mensajes[] = {
                "Hola",
                "buenos dias",
                "como estan",
                "que tal "
            };
            try {
                for (int i = 0;
                     i < mensajes.length;
                     i++) {
                    // Pausa por 4 seconds
                    Thread.sleep(4000);
                    // imprime un mensaje
                    mensajeHilo(mensajes[i]);
                }
            } catch (InterruptedException e) {
                mensajeHilo("No estaba terminado!");
            }
        }
    }

    public static void main(String args[])
        throws InterruptedException {

        // retardo, in milisengundos antes
        // interrumpimos el hilo ciclomensajes
        //  (default una hora ).
        long patience = 1000 * 60 * 60;

        // si hay argumento en linea de comandos, damos segundos a paciencia
        // in seconds.
        if (args.length > 0) {
            try {
                patience = Long.parseLong(args[0]) * 1000;
            } catch (NumberFormatException e) {
                System.err.println("el argumento debe se un entero.");
                System.exit(1);
            }
        }

        mensajeHilo("iniciando hilo ciclomensajes ");
        long startTime = System.currentTimeMillis();
        Thread t = new Thread(new ciclomensajes());
        t.start();

        mensajeHilo("Esperando que Hilo ciclomensajes termine");
        // ciclo hasta que el hilo  ciclomensajes salga
        // 
        while (t.isAlive()) {
            mensajeHilo("aun esperando ...");
            // Espera maximo 1 segundo para el hilo 
            //ciclomensaje termine
          
            t.join(1000);
            if (((System.currentTimeMillis() - startTime) > patience)
                  && t.isAlive()) {
                mensajeHilo("Cansado de esperar!");
                t.interrupt();
                // No debería tardar mucho ahora
                 // - espera indefinidamente
                t.join();
            }
        }
        mensajeHilo("Finalmente!");
    }
}
