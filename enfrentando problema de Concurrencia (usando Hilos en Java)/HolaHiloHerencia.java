

public class HolaHiloHerencia extends Thread {

    public void run() {
        System.out.println("Hola con Herencia!");
    }

    public static void main(String args[]) {
        (new HolaHiloHerencia()).start();
    }

}
