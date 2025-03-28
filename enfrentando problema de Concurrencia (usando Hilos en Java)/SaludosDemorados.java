

public class SaludosDemorados {
    public static void main(String args[])
        throws InterruptedException {
        String saludos[] = {
            "Hola como estas",
            "buenos dias",
            "hello",
            "Salut!"
        };

        for (int i = 0; i < saludos.length; i++) {
            //Pausa  4 segundos
            Thread.sleep(4000);
            //imprime el saludo 
            System.out.println(saludos[i]);
        }
    }
}

for (int i = 0; i < saludos.length; i++) {
            //Pausa  4 segundos
            Thread.sleep(4000);

    } catch (InterruptedException e) {
        // Hemos sifo interumpido, no hay mas mensajes
        return;
    }
    //imprime el saludo 
            System.out.println(saludos[i]);
        }
