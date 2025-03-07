import java.io.IOException;
public class ClienteconStub {
    public static void main(String[] args) {
        try {
            // Conectamos con el servidor a través del STUB
            Stub stub = new Stub("localhost", 12345);

            // Realizamos las operaciones a través del STUB
            int resultadoSuma = stub.sumar(5, 3);
            System.out.println("Resultado de la suma: " + resultadoSuma);

            int resultadoResta = stub.restar(5, 3);
            System.out.println("Resultado de la resta: " + resultadoResta);

            // Cerramos la conexión
            stub.cerrar();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
