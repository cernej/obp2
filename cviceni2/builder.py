class ServerConfiguration:
    def __init__(self):
        self.host = None
        self.port = None
        self.ssl = None
        self.timeout = None
        self.max_connections = None
        self.logging = None

    def set_host(self, host):
        self.host = host
        return self

    def set_port(self, port):
        self.port = port
        return self

    def set_ssl(self, ssl):
        self.ssl = ssl
        return self
    
    def set_timeout(self, timeout):
        self.timeout = timeout
        return self

    def set_max_connections(self, max_connections):
        self.max_connections = max_connections
        return self
    
    def set_logging(self, logging):
        self.logging = logging
        return self

    def __str__(self) -> str:
        return (
            f"ServerConfiguration(host='{self.host}', port={self.port}, ssl={self.ssl}, "
            f"timeout={self.timeout}, max_connections={self.max_connections}, logging={self.logging})"
        )


def pripoj_se_k_serveru(config):
    print(f"pripojuju se k serveru {config.host}:{config.port}")


if __name__ == "__main__":
    pripoj_se_k_serveru(ServerConfiguration().set_host("0.0.0.0").set_port(443).set_max_connections(5))
    pripoj_se_k_serveru(ServerConfiguration().set_host("127.0.0.1").set_port(80).set_max_connections(5))