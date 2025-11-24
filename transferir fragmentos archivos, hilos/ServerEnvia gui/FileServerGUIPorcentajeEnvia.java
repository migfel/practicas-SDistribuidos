import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class FileServerGUIPorcentajeEnvia  extends JFrame {

    private JTextField txtPort;
    private JTextField txtFile;
    private JButton btnBrowse;
    private JButton btnStart;
    private JProgressBar progressBar;
    private JTextArea txtLog;

    private ServerSocket serverSocket;
    private volatile boolean running = false;
    private File selectedFile;

    public FileServerGUIPorcentajeEnvia() {
        setTitle("Servidor - Envío de Video");
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

        // Puerto
        gbc.gridx = 0; gbc.gridy = 0; gbc.weightx = 0;
        topPanel.add(new JLabel("Puerto:"), gbc);
        txtPort = new JTextField("12345");
        gbc.gridx = 1; gbc.gridy = 0; gbc.weightx = 1.0;
        topPanel.add(txtPort, gbc);

        // Archivo
        gbc.gridx = 0; gbc.gridy = 1; gbc.weightx = 0;
        topPanel.add(new JLabel("Archivo de video:"), gbc);
        txtFile = new JTextField();
        txtFile.setEditable(false);
        gbc.gridx = 1; gbc.gridy = 1; gbc.weightx = 1.0;
        topPanel.add(txtFile, gbc);

        btnBrowse = new JButton("Seleccionar...");
        btnBrowse.addActionListener(this::onBrowseFile);
        gbc.gridx = 2; gbc.gridy = 1; gbc.weightx = 0;
        topPanel.add(btnBrowse, gbc);

        btnStart = new JButton("Esperar cliente y enviar");
        btnStart.addActionListener(e -> onStartServer());
        gbc.gridx = 1; gbc.gridy = 2; gbc.gridwidth = 2;
        topPanel.add(btnStart, gbc);
        gbc.gridwidth = 1;

        progressBar = new JProgressBar(0, 100);
        progressBar.setStringPainted(true);

        txtLog = new JTextArea();
        txtLog.setEditable(false);
        JScrollPane scrollLog = new JScrollPane(txtLog);
        scrollLog.setPreferredSize(new Dimension(600, 180));

        setLayout(new BorderLayout());
        add(topPanel, BorderLayout.NORTH);
        add(progressBar, BorderLayout.CENTER);
        add(scrollLog, BorderLayout.SOUTH);
    }

    private void onBrowseFile(ActionEvent e) {
        JFileChooser chooser = new JFileChooser();
        int result = chooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            selectedFile = chooser.getSelectedFile();
            txtFile.setText(selectedFile.getAbsolutePath());
            log("Archivo seleccionado: " + selectedFile.getName() +
                    " (" + selectedFile.length() + " bytes)");
        }
    }

    private void onStartServer() {
        if (running) {
            JOptionPane.showMessageDialog(this, "El servidor ya está en ejecución.",
                    "Info", JOptionPane.INFORMATION_MESSAGE);
            return;
        }

        if (selectedFile == null) {
            JOptionPane.showMessageDialog(this, "Selecciona primero un archivo de video.",
                    "Error", JOptionPane.ERROR_MESSAGE);
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
        btnBrowse.setEnabled(false);
        txtPort.setEnabled(false);
        log("Iniciando servidor en puerto " + port + "...");
        log("Esperando a que un cliente se conecte...");

        new Thread(() -> startServer(port, selectedFile)).start();
    }

    private void startServer(int port, File file) {
        try {
            serverSocket = new ServerSocket(port);
            try (Socket client = serverSocket.accept()) {
                log("Cliente conectado desde: " + client.getInetAddress());

                sendFileToClient(client, file);

            } finally {
                if (serverSocket != null && !serverSocket.isClosed()) {
                    serverSocket.close();
                }
            }

            log("Servidor finalizó envío y cerró conexión.");

        } catch (IOException e) {
            log("Error en el servidor: " + e.getMessage());
            e.printStackTrace();
        } finally {
            running = false;
            SwingUtilities.invokeLater(() -> {
                btnStart.setEnabled(true);
                btnBrowse.setEnabled(true);
                txtPort.setEnabled(true);
            });
        }
    }

    private void sendFileToClient(Socket client, File file) {
        long fileSize = file.length();
        if (!file.exists()) {
            log("El archivo no existe: " + file.getAbsolutePath());
            return;
        }

        try (DataOutputStream dos = new DataOutputStream(client.getOutputStream());
             FileInputStream fis = new FileInputStream(file)) {

            log("Enviando archivo: " + file.getName() + " (" + fileSize + " bytes)");

            // 1. Enviar nombre del archivo
            dos.writeUTF(file.getName());

            // 2. Enviar tamaño del archivo
            dos.writeLong(fileSize);

            // 3. Enviar contenido
            byte[] buffer = new byte[8192];
            int bytesRead;
            long totalSent = 0;
            int lastPercent = 0;
            updateProgress(0);

            while ((bytesRead = fis.read(buffer)) != -1) {
                dos.write(buffer, 0, bytesRead);
                totalSent += bytesRead;

                if (fileSize > 0) {
                    int percent = (int) ((totalSent * 100) / fileSize);
                    if (percent != lastPercent) {
                        lastPercent = percent;
                        updateProgress(percent);
                    }
                }
            }

            updateProgress(100);
            log("Envío completado.");

        } catch (IOException e) {
            log("Error enviando archivo: " + e.getMessage());
            e.printStackTrace();
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
            FileServerGUIPorcentajeEnvia gui = new FileServerGUIPorcentajeEnvia();
            gui.setVisible(true);
        });
    }
}
