package fileshare;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.stub.StreamObserver;

import java.io.File;
import java.io.FileInputStream;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

import com.google.protobuf.ByteString;

public class FileClientPorcentajeGrpc {

    public static void main(String[] args) {
        String host = "localhost";
        int port = 12345; // igual que en el servidor
        String filePath = "uno.mp4"; // nombre del archivo a enviar

        File file = new File(filePath);

        if (!file.exists()) {
            System.out.println("El archivo no existe: " + file.getAbsolutePath());
            return;
        }

        long fileSize = file.length();
        System.out.println("Iniciando envío de: " + file.getName());
        System.out.println("Tamaño: " + fileSize + " bytes");

        ManagedChannel channel = ManagedChannelBuilder
                .forAddress(host, port)
                .usePlaintext()
                .build();

        FileServiceGrpc.FileServiceStub stub = FileServiceGrpc.newStub(channel);
        CountDownLatch latch = new CountDownLatch(1);

        StreamObserver<UploadStatus> responseObserver = new StreamObserver<UploadStatus>() {
            @Override
            public void onNext(UploadStatus value) {
                System.out.println("\nRespuesta del servidor: " + value.getMessage());
            }

            @Override
            public void onError(Throwable t) {
                t.printStackTrace();
                latch.countDown();
            }

            @Override
            public void onCompleted() {
                System.out.println("Envío completado (gRPC).");
                latch.countDown();
            }
        };

        StreamObserver<FileChunk> requestObserver = stub.upload(responseObserver);

        try (FileInputStream fis = new FileInputStream(file)) {
            byte[] buffer = new byte[64 * 1024]; // 64 KB
            int bytesRead;
            long sentBytes = 0;

            // Primer chunk con meta-datos
            bytesRead = fis.read(buffer);
            if (bytesRead == -1) {
                System.out.println("Archivo vacío, nada que enviar.");
                requestObserver.onCompleted();
            } else {
                FileChunk firstChunk = FileChunk.newBuilder()
                        .setFileName(file.getName())
                        .setFileSize(fileSize)
                        .setData(ByteString.copyFrom(buffer, 0, bytesRead))
                        .build();

                requestObserver.onNext(firstChunk);
                sentBytes += bytesRead;

                if (fileSize > 0) {
                    int porcentaje = (int) ((sentBytes * 100) / fileSize);
                    System.out.print("\rProgreso de envío: " + porcentaje + "%");
                }

                // Resto de chunks solo con data
                while ((bytesRead = fis.read(buffer)) != -1) {
                    FileChunk chunk = FileChunk.newBuilder()
                            .setFileName("")   // opcional
                            .setFileSize(0)    // opcional
                            .setData(ByteString.copyFrom(buffer, 0, bytesRead))
                            .build();

                    requestObserver.onNext(chunk);

                    sentBytes += bytesRead;
                    if (fileSize > 0) {
                        int porcentaje = (int) ((sentBytes * 100) / fileSize);
                        System.out.print("\rProgreso de envío: " + porcentaje + "%");
                    }
                }

                requestObserver.onCompleted();
            }

            // Esperar respuesta del servidor
            latch.await(1, TimeUnit.MINUTES);

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            channel.shutdown();
            try {
                channel.awaitTermination(5, TimeUnit.SECONDS);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
