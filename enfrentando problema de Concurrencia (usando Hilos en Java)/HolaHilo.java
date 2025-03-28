

public class HolaHilo implements Runnable {

    public void run() {
        System.out.println("Hola desde un Hilo!");
    }

    public static void main(String args[]) 
    {
        (new Thread(new HolaHilo())).start();
    }

}
