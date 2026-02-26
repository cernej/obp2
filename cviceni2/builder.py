class ServerConfiguration:
    def __init__(
        self,
        host: str,
        port: int,
        ssl: bool,
        timeout: int,
        max_connections: int,
        logging: bool,
    ):
        self.host = host
        self.port = port
        self.ssl = ssl
        self.timeout = timeout
        self.max_connections = max_connections
        self.logging = logging

    def __str__(self) -> str:
        return (
            f"ServerConfiguration(host='{self.host}', port={self.port}, ssl={self.ssl}, "
            f"timeout={self.timeout}, max_connections={self.max_connections}, logging={self.logging})"
        )


if __name__ == "__main__":
    config = (
        ServerConfiguration(
            host="0.0.0.0",
            port=443,
            ssl=True,
            timeout=10,
            max_connections=100,
            logging=True
        )
    )
    print(config)