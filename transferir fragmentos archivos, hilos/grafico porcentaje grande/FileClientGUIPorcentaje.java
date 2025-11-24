import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.io.*;
import java.net.Socket;

public class FileClientGUIPorcentaje extends JFrame {

    private JTextField txtHost;
    private JTextField txtPort;
    private JTextField txtFile;
    private JProgressBar progressBar;
    private JTextArea txtLog;
    private File selectedFile;

    public FileClientGUIPorcentaje() {
        setTitle("Cliente de Envío de Archivos");
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

        // Archivo
        gbc.gridx = 0; gbc.gridy = 2; gbc.weightx = 0;
        topPanel.add(new JLabel("Archivo:"), gbc);
        txtFile = new JTextField();
        txtFile.setEditable(false);
        gbc.gridx = 1; gbc.gridy = 2; gbc.weightx = 1;
        topPanel.add(txtFile, gbc);

        JButton btnBrowse = new JButton("Seleccionar...");
        btnBrowse.addActionListener(this::onBrowseFile);
        gbc.gridx = 2; gbc.gridy = 2; gbc.weightx = 0;
        topPanel.add(btnBrowse, gbc);

        // Botón Enviar
        JButton btnSend = new JButton("Enviar archivo");
        btnSend.addActionListener(this::onSendFile);
        gbc.gridx = 1; gbc.gridy = 3; gbc.gridwidth = 2;
        topPanel.add(btnSend, gbc);
        gbc.gridwidth = 1;

        // Barra de progreso
        progressBar = new JProgressBar(0, 100);
        progressBar.setStringPainted(true);

        // Área de log
        txtLog = new JTextArea();
        txtLog.setEditable(false);
        JScrollPane scrollLog = new JScrollPane(txtLog);

        // Layout principal
        setLayout(new BorderLayout());
        add(topPanel, BorderLayout.NORTH);
        add(progressBar, BorderLayout.CENTER);
        add(scrollLog, BorderLayout.SOUTH);

        // Ajuste de proporciones
        scrollLog.setPreferredSize(new Dimension(600, 150));
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

    private void onSendFile(ActionEvent e) {
        if (selectedFile == null) {
            JOptionPane.showMessageDialog(this, "Primero selecciona un archivo.",
                    "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        String host = txtHost.getText().trim();
        int port;

        try {
            port = Integer.parseInt(txtPort.getText().trim());
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Puerto inválido.",
                    "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        // Ejecutar el envío en un hilo separado para no bloquear la GUI
        new Thread(() -> sendFile(host, port, selectedFile)).start();
    }

    private void sendFile(String host, int port, File file) {
        long fileSize = file.length();

        if (!file.exists()) {
            log("El archivo no existe: " + file.getAbsolutePath());
            return;
        }

        try (Socket socket = new Socket(host, port);
             DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
             FileInputStream fis = new FileInputStream(file)) {

            log("Conectado a " + host + ":" + port);
            log("Enviando archivo: " + file.getName() + " (" + fileSize + " bytes)");

            // 1. Enviar nombre del archivo
            dos.writeUTF(file.getName());

            // 2. Enviar tamaño del archivo
            dos.writeLong(fileSize);

            // 3. Enviar contenido del archivo
            byte[] buffer = new byte[8192]; // 8 KB
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

        } catch (Exception ex) {
            log("Error en el cliente: " + ex.getMessage());
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
            FileClientGUIPorcentaje gui = new FileClientGUIPorcentaje();
            gui.setVisible(true);
        });
    }
}
