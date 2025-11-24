import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.io.*;
import java.net.Socket;
import java.awt.Desktop;

public class FileClientGUIPorcentajeRecibe extends JFrame {

    private JTextField txtHost;
    private JTextField txtPort;
    private JTextField txtOutputDir;
    private JProgressBar progressBar;
    private JTextArea txtLog;

    public FileClientGUIPorcentajeRecibe() {
        setTitle("Cliente - Recepción y Reproducción de Video");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(650, 350);
        setLocationRelativeTo(null);

        initComponents();
    }

    private void initComponents() {
        JPanel topPanel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(4, 4, 4, 4);
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.weightx = 1.0;

        // Host
        gbc.gridx = 0; gbc.gridy = 0; gbc.weightx = 0;
        topPanel.add(new JLabel("Host:"), gbc);
        txtHost = new JTextField("localhost");
        gbc.gridx = 1; gbc.gridy = 0; gbc.weightx = 1;
        topPanel.add(txtHost, gbc);

        // Puerto
        gbc.gridx = 0; gbc.gridy = 1; gbc.weightx = 0;
        topPanel.add(new JLabel("Puerto:"), gbc);
        txtPort = new JTextField("12345");
        gbc.gridx = 1; gbc.gridy = 1; gbc.weightx = 1;
        topPanel.add(txtPort, gbc);

        // Directorio de salida (opcional, por defecto carpeta actual)
        gbc.gridx = 0; gbc.gridy = 2; gbc.weightx = 0;
        topPanel.add(new JLabel("Directorio salida (opcional):"), gbc);
        txtOutputDir = new JTextField();
        gbc.gridx = 1; gbc.gridy = 2; gbc.weightx = 1;
        topPanel.add(txtOutputDir, gbc);

        JButton btnSelectDir = new JButton("Elegir...");
        btnSelectDir.addActionListener(this::onSelectOutputDir);
        gbc.gridx = 2; gbc.gridy = 2; gbc.weightx = 0;
        topPanel.add(btnSelectDir, gbc);

        // Botón conectar
        JButton btnReceive = new JButton("Conectar y recibir video");
        btnReceive.addActionListener(this::onReceiveFile);
        gbc.gridx = 1; gbc.gridy = 3; gbc.gridwidth = 2;
        topPanel.add(btnReceive, gbc);
        gbc.gridwidth = 1;

        // Barra de progreso
        progressBar = new JProgressBar(0, 100);
        progressBar.setStringPainted(true);

        // Área de log
        txtLog = new JTextArea();
        txtLog.setEditable(false);
        JScrollPane scrollLog = new JScrollPane(txtLog);

        setLayout(new BorderLayout());
        add(topPanel, BorderLayout.NORTH);
        add(progressBar, BorderLayout.CENTER);
        add(scrollLog, BorderLayout.SOUTH);

        scrollLog.setPreferredSize(new Dimension(600, 150));
    }

    private void onSelectOutputDir(ActionEvent e) {
        JFileChooser chooser = new JFileChooser();
        chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        int result = chooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            File dir = chooser.getSelectedFile();
            txtOutputDir.setText(dir.getAbsolutePath());
            log("Directorio de salida seleccionado: " + dir.getAbsolutePath());
        }
    }

    private void onReceiveFile(ActionEvent e) {
        String host = txtHost.getText().trim();
        int port;

        try {
            port = Integer.parseInt(txtPort.getText().trim());
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Puerto inválido.",
                    "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        new Thread(() -> receiveFile(host, port)).start();
    }

    private void receiveFile(String host, int port) {
        try (Socket socket = new Socket(host, port);
             DataInputStream dis = new DataInputStream(socket.getInputStream())) {

            log("Conectado a servidor " + host + ":" + port);

            // 1. Leer nombre del archivo
            String fileName = dis.readUTF();

            // 2. Leer tamaño del archivo
            long fileSize = dis.readLong();

            log("Recibiendo archivo: " + fileName + " (" + fileSize + " bytes)");

            // Directorio de salida
            File outputDir;
            if (txtOutputDir.getText().trim().isEmpty()) {
                outputDir = new File("."); // actual
            } else {
                outputDir = new File(txtOutputDir.getText().trim());
                if (!outputDir.exists()) {
                    outputDir.mkdirs();
                }
            }

            File outFile = new File(outputDir, "received_" + fileName);
            log("Guardando como: " + outFile.getAbsolutePath());

            try (FileOutputStream fos = new FileOutputStream(outFile)) {
                byte[] buffer = new byte[8192]; // 8 KB
                long totalRead = 0;
                int bytesRead;
                int lastPercent = 0;
                updateProgress(0);

                // Umbral para empezar la reproducción (5 MB o tamaño total si es menor)
                long bufferToStart = Math.min(fileSize, 5L * 1024 * 1024);
                boolean playbackStarted = false;

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

                    // Iniciar reproducción cuando haya suficiente buffer
                    if (!playbackStarted && totalRead >= bufferToStart) {
                        playbackStarted = true;
                        startPlayback(outFile);
                    }
                }

                updateProgress(100);
                log("Recepción completada.");

                if (!playbackStarted) {
                    // Si el archivo era pequeño, iniciamos reproducción al final
                    startPlayback(outFile);
                }
            }

        } catch (IOException ex) {
            log("Error recibiendo archivo: " + ex.getMessage());
            ex.printStackTrace();
        }
    }

    private void startPlayback(File videoFile) {
        try {
            if (Desktop.isDesktopSupported()) {
                log("Iniciando reproducción de: " + videoFile.getName());
                new Thread(() -> {
                    try {
                        Desktop.getDesktop().open(videoFile);
                    } catch (IOException ex) {
                        log("No se pudo abrir el reproductor: " + ex.getMessage());
                        ex.printStackTrace();
                    }
                }).start();
            } else {
                log("Desktop API no soportada en este sistema. No puedo abrir el video automáticamente.");
            }
        } catch (Exception ex) {
            log("Error al intentar reproducir el video: " + ex.getMessage());
            ex.printStackTrace();
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

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            FileClientGUIPorcentajeRecibe gui = new FileClientGUIPorcentajeRecibe();
            gui.setVisible(true);
        });
    }
}
