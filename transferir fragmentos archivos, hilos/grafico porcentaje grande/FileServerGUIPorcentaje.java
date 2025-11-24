import javax.swing.*;
import java.awt.*;
import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class FileServerGUIPorcentaje extends JFrame {

    private JTextField txtPort;
    private JButton btnStart;
    private JProgressBar progressBar;
    private JTextArea txtLog;

    private ServerSocket serverSocket;
    private volatile boolean running = false;

    public FileServerGUIPorcentaje() {
        setTitle("Servidor de Recepción de Archivos");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(600, 350);
        setLocationRelativeTo(null);

        initComponents();
    }

    private void initComponents() {
        JPanel topPanel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(4, 4, 4, 4);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        gbc.gridx = 0; gbc.gridy = 0; gbc.weightx = 0;
        topPanel.add(new JLabel("Puerto:"), gbc);
        txtPort = new JTextField("12345");
        gbc.gridx = 1; gbc.gridy = 0; gbc.weightx = 1.0;
        topPanel.add(txtPort, gbc);

        btnStart = new JButton("Iniciar servidor");
        btnStart.addActionListener(e -> onStartServer());
        gbc.gridx = 2; gbc.gridy = 0; gbc.weightx = 0;
        topPanel.add(btnStart, gbc);

        progressBar = new JProgressBar(0, 100);
        progressBar.setStringPainted(true);

        txtLog = new JTextArea();
        txtLog.setEditable(false);
        JScrollPane scrollLog = new JScrollPane(txtLog);
        scrollLog.setPreferredSize(new Dimension(600, 200));

        setLayout(new BorderLayout());
        add(topPanel, BorderLayout.NORTH);
        add(progressBar, BorderLayout.CENTER);
        add(scrollLog, BorderLayout.SOUTH);
    }

    private void onStartServer() {
        if (running) {
            JOptionPane.showMessageDialog(this, "El servidor ya está en ejecución.",
                    "Info", JOptionPane.INFORMATION_MESSAGE);
            return;
        }

        int port;
        try {
            port = Integer.parseInt(txtPort.getText().trim());
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Puerto inválido.",
                    "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        running = true;
        btnStart.setEnabled(false);
        log("Iniciando servidor en puerto " + port + "...");

        new Thread(() -> startServer(port)).start();
    }

    private void startServer(int port) {
        try {
            serverSocket = new ServerSocket(port);
            log("Servidor listo en puerto " + port + "...");

            while (running) {
                Socket client = serverSocket.accept();
                log("Cliente conectado: " + client.getInetAddress());
                // Para cada cliente, se lanza un hilo con handler
                new Thread(new Handler(client)).start();
            }

        } catch (IOException e) {
            log("Error en el servidor: " + e.getMessage());
            e.printStackTrace();
        } finally {
            running = false;
            SwingUtilities.invokeLater(() -> btnStart.setEnabled(true));
        }
    }

    private void updateProgress(int value) {
        SwingUtilities.invokeLater(() -> progressBar.setValue(value));
    }

    private void log(String message) {
        SwingUtilities.invokeLater(() -> {
            txtLog.append(message + "\n");
            txtLog.setCaretPosition(txtLog.getDocument().getLength());
        });
    }

    // Handler interno para manejar cada cliente
    private class Handler implements Runnable {
        private final Socket socket;

        public Handler(Socket socket) {
            this.socket = socket;
        }

        public void run() {
            try (DataInputStream dis = new DataInputStream(socket.getInputStream())) {

                // 1. Leer nombre del archivo
                String fileName = dis.readUTF();

                // 2. Leer tamaño del archivo
                long fileSize = dis.readLong();

                log("Recibiendo archivo: " + fileName + " (" + fileSize + " bytes)");

                try (FileOutputStream fos = new FileOutputStream("received_" + fileName)) {
                    byte[] buffer = new byte[8192]; // 8 KB
                    long totalRead = 0;
                    int bytesRead;
                    int lastPercent = 0;
                    updateProgress(0);

                    // 3. Leer exactamente fileSize bytes
                    while (totalRead < fileSize && (bytesRead = dis.read(buffer)) != -1) {
                        fos.write(buffer, 0, bytesRead);
                        totalRead += bytesRead;

                        if (fileSize > 0) {
                            int percent = (int) ((totalRead * 100) / fileSize);
                            if (percent != lastPercent) {
                                lastPercent = percent;
                                updateProgress(percent);
                            }
                        }
                    }

                    updateProgress(100);
                    log("Recepción completada de: " + fileName);
                }

                socket.close();

            } catch (Exception e) {
                log("Error manejando cliente: " + e.getMessage());
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            FileServerGUIPorcentaje gui = new FileServerGUIPorcentaje();
            gui.setVisible(true);
        });
    }
}
