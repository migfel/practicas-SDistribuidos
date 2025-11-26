package fileshare;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;

import java.io.FileOutputStream;
import java.io.IOException;

public class FileServerPorcentajeGrpc {

    private final int port;

    public FileServerPorcentajeGrpc(int port) {
        this.port = port;
    }

    public void start() throws IOException, InterruptedException {
        Server server = ServerBuilder.forPort(port)
                .addService(new FileServiceImpl())
                .build()
                .start();

        System.out.println("Servidor gRPC listo en puerto " + port + "...");
        server.awaitTermination();
    }

    public static void main(String[] args) throws IOException, InterruptedException {
        int port = 12345; // igual que tu versión con sockets
        new FileServerPorcentajeGrpc(port).start();
    }

    // Implementación del servicio
    static class FileServiceImpl extends FileServiceGrpc.FileServiceImplBase {

        @Override
        public StreamObserver<FileChunk> upload(StreamObserver<UploadStatus> responseObserver) {
            return new StreamObserver<FileChunk>() {

                private FileOutputStream fos;
                private String fileName = null;
                private long fileSize = 0;
                private long receivedBytes = 0;

                @Override
                public void onNext(FileChunk chunk) {
                    try {
                        // Primer mensaje: obtenemos metadatos y abrimos archivo
                        if (fos == null) {
                            fileName = chunk.getFileName();
                            if (fileName == null || fileName.isEmpty()) {
                                fileName = "archivo_recibido.dat";
                            }

                            fileSize = chunk.getFileSize();
                            fos = new FileOutputStream(fileName);

                            System.out.println("Iniciando recepción de archivo: " + fileName);
                            System.out.println("Tamaño declarado: " + fileSize + " bytes");
                        }

                        // Escribimos los datos
                        byte[] data = chunk.getData().toByteArray();
                        if (data.length > 0) {
                            fos.write(data);
                            receivedBytes += data.length;

                            if (fileSize > 0) {
                                int porcentaje = (int) ((receivedBytes * 100) / fileSize);
                                System.out.print("\rProgreso de recepción: " + porcentaje + "%");
                            } else {
                                System.out.print("\rRecibidos: " + receivedBytes + " bytes");
                            }
                        }

                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }

                @Override
                public void onError(Throwable t) {
                    t.printStackTrace();
                    try {
                        if (fos != null) fos.close();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }

                @Override
                public void onCompleted() {
                    try {
                        if (fos != null) fos.close();
                        System.out.println("\nRecepción completada de: " + fileName);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                    UploadStatus status = UploadStatus.newBuilder()
                            .setOk(true)
                            .setMessage("Archivo " + fileName + " recibido correctamente.")
                            .build();

                    responseObserver.onNext(status);
                    responseObserver.onCompleted();
                }
            };
        }
    }
}
