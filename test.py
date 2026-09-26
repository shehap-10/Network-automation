from flask import Flask, request, jsonify, send_from_directory
import paramiko
import time

app = Flask(__name__)


@app.route("/")
def home():
    return send_from_directory(".", "home.html")


@app.route("/connect", methods=["POST"])
def connect():

    # Get data from HTML/JavaScript
    data = request.json

    HOST = data["host"]
    USERNAME = data["username"]
    PASSWORD = data["password"]

    PORT = 22

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        transport = paramiko.Transport((HOST, PORT))

        # Configure legacy Cisco SSH algorithms
        security = transport.get_security_options()
        security.kex = ("diffie-hellman-group14-sha1",)
        security.key_types = ("ssh-rsa",)
        security.ciphers = (
            "aes128-ctr",
            "aes192-ctr",
            "aes256-ctr"
        )
        security.digests = ("hmac-sha1",)

        # Connect using values received from HTML
        transport.connect(
            username=USERNAME,
            password=PASSWORD
        )

        ssh._transport = transport

        print("Connected successfully!")

        # Open Cisco CLI
        shell = ssh.invoke_shell()

        time.sleep(1)

        shell.send("terminal length 0\n")
        time.sleep(1)

        shell.send("show running-config\n")
        time.sleep(3)

        # Receive configuration
        output = b""

        while shell.recv_ready():
            output += shell.recv(65535)
            time.sleep(0.2)

        # Save configuration
        filename = f"router_config_{HOST}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(output.decode("utf-8", errors="ignore"))

        ssh.close()

        return jsonify({
            "message": "Connected successfully!",
            "file": filename
        })

    except Exception as e:

        ssh.close()

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run()